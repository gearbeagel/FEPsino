from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from decimal import Decimal
from unittest.mock import patch, MagicMock
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from .models import Symbol, Spin
from .services import ReelService, SlotMachineService
from .serializers import SpinSerializer, SymbolSerializer, SpinRequestSerializer

User = get_user_model()


class ReelServiceTestCase(TestCase):
    """Tests for the ReelService class"""
    
    def setUp(self):
        # Create test symbols
        self.symbol1 = Symbol.objects.create(name='star', payout_multiplier=2.0)
        self.symbol2 = Symbol.objects.create(name='heart', payout_multiplier=1.5)
        self.symbol3 = Symbol.objects.create(name='cherry', payout_multiplier=1.2)
        self.symbol4 = Symbol.objects.create(name='gem', payout_multiplier=3.0)
        self.symbol5 = Symbol.objects.create(name='citrus', payout_multiplier=1.0)

        # Initialize ReelService with test symbols
        self.symbols = Symbol.objects.all()
        self.reel_service = ReelService(self.symbols)

    def test_generate_spin(self):
        """Test that generate_spin returns a valid spin result."""
        # Test with default parameters (5 reels, 3 rows)
        result = self.reel_service.generate_spin()

        # Check that result has 5 reels by default
        self.assertEqual(len(result), 5)
        # Check that each reel has 3 symbols by default
        for reel_num, symbols in result.items():
            self.assertEqual(len(symbols), 3)
            # Check that all symbols are valid indices
            for symbol in symbols:
                self.assertIn(symbol, range(5))  # We have 5 symbols (0-4)

        # Test with custom parameters
        result = self.reel_service.generate_spin(num_reels=3, visible_rows=2)
        self.assertEqual(len(result), 3)
        for reel_num, symbols in result.items():
            self.assertEqual(len(symbols), 2)

    def test_extract_horizontal_values(self):
        """Test that _extract_horizontal_values correctly extracts values."""
        result = {
            0: [0, 1, 2],
            1: [1, 2, 0],
            2: [2, 0, 1]
        }
        horizontal_values = self.reel_service._extract_horizontal_values(result)
        expected = [
            [0, 1, 2],
            [1, 2, 0],
            [2, 0, 1]
        ]
        self.assertEqual(horizontal_values, expected)

    def test_transpose_matrix(self):
        """Test that _transpose_matrix correctly transposes a matrix."""
        matrix = [
            [0, 1, 2],
            [1, 2, 0],
            [2, 0, 1]
        ]
        transposed = self.reel_service._transpose_matrix(matrix)
        expected = [
            [2, 1, 0],
            [0, 2, 1],
            [1, 0, 2]
        ]
        self.assertEqual(transposed, expected)

    def test_reverse_rows(self):
        """Test that _reverse_rows correctly reverses each row in a matrix."""
        matrix = [
            [0, 1, 2],
            [1, 2, 0],
            [2, 0, 1]
        ]
        reversed_rows = self.reel_service._reverse_rows(matrix)
        expected = [
            [2, 1, 0],
            [0, 2, 1],
            [1, 0, 2]
        ]
        self.assertEqual(reversed_rows, expected)

    def test_flip_horizontal(self):
        """Test that flip_horizontal correctly transforms the data."""
        # Create a test result
        result = {
            0: [0, 1, 2],
            1: [1, 2, 0],
            2: [2, 0, 1]
        }

        horizontal = self.reel_service.flip_horizontal(result)

        # Expected result after transformation
        expected = [
            [2, 0, 1],
            [1, 2, 0],
            [0, 1, 2]
        ]

        self.assertEqual(horizontal, expected)

    def test_longest_seq(self):
        """Test that longest_seq finds the longest consecutive sequence."""
        # Test with a simple sequence
        hit = [0, 1, 2, 4, 5, 6]
        longest = self.reel_service.longest_seq(hit)
        self.assertEqual(longest, [0, 1, 2])

        # Test with another sequence
        hit = [1, 3, 4, 5, 7, 8]
        longest = self.reel_service.longest_seq(hit)
        self.assertEqual(longest, [3, 4, 5])

        # Test with no consecutive sequence
        hit = [1, 3, 5, 7, 9]
        longest = self.reel_service.longest_seq(hit)
        self.assertEqual(longest, [])

        # Test with empty input
        hit = []
        longest = self.reel_service.longest_seq(hit)
        self.assertEqual(longest, [])

        # Test with a single element
        hit = [5]
        longest = self.reel_service.longest_seq(hit)
        self.assertEqual(longest, [])

    def test_find_winning_combinations(self):
        """Test that _find_winning_combinations correctly identifies winning combinations."""
        horizontal = [
            [0, 0, 0, 1, 2],  # Three stars in a row
            [1, 2, 3, 4, 0],  # No winning combinations
            [2, 2, 2, 2, 1]   # Four cherries in a row
        ]

        wins = self.reel_service._find_winning_combinations(horizontal)
        
        # We should have wins in rows 1 and 3
        self.assertIn(1, wins)
        self.assertIn(3, wins)
        
        # The winning symbols should be 'star' and 'cherry'
        self.assertEqual(wins[1][0], 'star')
        self.assertEqual(wins[3][0], 'cherry')
        
        # The winning indices should match
        self.assertEqual(wins[1][1], [0, 1, 2])
        self.assertEqual(wins[3][1], [0, 1, 2, 3])

    def test_check_wins(self):
        """Test that check_wins correctly identifies winning combinations."""
        # Create a test result with a winning combination
        result = {
            0: [0, 1, 2],
            1: [0, 1, 2],
            2: [0, 1, 2],
            3: [3, 4, 0],
            4: [3, 4, 0]
        }

        wins = self.reel_service.check_wins(result)

        # We should have a win in row 1 (star symbols)
        self.assertIsNotNone(wins)
        self.assertIn(1, wins)  # Row 1 should have a win
        self.assertEqual(wins[1][0], 'star')  # The winning symbol should be 'star'
        self.assertEqual(wins[1][1], [0, 1, 2])  # The winning indices

        # Test with no winning combinations
        result = {
            0: [0, 1, 2],
            1: [3, 4, 0],
            2: [1, 2, 3],
            3: [4, 0, 1],
            4: [2, 3, 4]
        }

        wins = self.reel_service.check_wins(result)
        self.assertIsNone(wins)

    def test_get_symbol_multiplier(self):
        """Test that _get_symbol_multiplier returns the correct multiplier."""
        # Test with existing symbol
        multiplier = self.reel_service._get_symbol_multiplier('star')
        self.assertEqual(multiplier, Decimal('2.0'))

        # Test with non-existent symbol (should return default multiplier)
        multiplier = self.reel_service._get_symbol_multiplier('nonexistent')
        self.assertEqual(multiplier, Decimal('1.0'))

    def test_calculate_win_payout_single_win(self):
        """Test that _calculate_win_payout calculates correct payout for a single win."""
        symbol_name = 'star'  # 2.0 multiplier
        indices = [0, 1, 2]  # 3 symbols
        bet_amount = Decimal('10.00')
        
        # Expected payout: 10 * 3 * 2.0 = 60
        expected_payout = Decimal('60.00')
        payout = self.reel_service._calculate_win_payout(symbol_name, indices, bet_amount)
        
        self.assertEqual(payout, expected_payout)

    def test_calculate_payout(self):
        """Test that calculate_payout correctly calculates the total payout."""
        # Create a test win data with multiple wins
        win_data = {
            1: ['star', [0, 1, 2]],  # 3 stars (multiplier 2.0) in row 1
            3: ['cherry', [1, 2, 3, 4]]  # 4 cherries (multiplier 1.2) in row 3
        }

        bet_amount = Decimal('10.00')
        payout = self.reel_service.calculate_payout(win_data, bet_amount)

        # Expected payout: (10 * 3 * 2.0) + (10 * 4 * 1.2) = 60 + 48 = 108
        expected_payout = Decimal('108.00')
        self.assertEqual(payout, expected_payout)

        # Test with no win data
        payout = self.reel_service.calculate_payout(None, bet_amount)
        self.assertEqual(payout, Decimal('0.00'))

        # Test with empty win data
        payout = self.reel_service.calculate_payout({}, bet_amount)
        self.assertEqual(payout, Decimal('0.00'))


class MockUserProfileModel:
    """Mock user profile for testing SlotMachineService"""
    def __init__(self, balance=Decimal('100.00')):
        self.balance = balance
    
    def deduct_balance(self, amount):
        self.balance -= amount
        
    def add_balance(self, amount):
        self.balance += amount


class SlotMachineServiceTestCase(TestCase):
    """Tests for the SlotMachineService class"""
    
    def setUp(self):
        # Create test user with profile
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        
        # Create mock profile
        self.user.profile = MockUserProfileModel(Decimal('100.00'))
        
        # Add balance, total_wager, and total_won attributes to user
        self.user.total_wager = Decimal('0.00')
        self.user.total_won = Decimal('0.00')
        self.user.save()

        # Create test symbols
        Symbol.objects.create(name='star', payout_multiplier=2.0)
        Symbol.objects.create(name='heart', payout_multiplier=1.5)
        Symbol.objects.create(name='cherry', payout_multiplier=1.2)
        Symbol.objects.create(name='gem', payout_multiplier=3.0)
        Symbol.objects.create(name='citrus', payout_multiplier=1.0)

        # Initialize SlotMachineService
        self.slot_service = SlotMachineService()

    def test_update_user_balance_for_bet(self):
        """Test that _update_user_balance_for_bet correctly updates the user's balance."""
        bet_amount = Decimal('10.00')
        result = self.slot_service._update_user_balance_for_bet(self.user, bet_amount)
        
        # Check that the balance was updated
        self.assertTrue(result)
        self.assertEqual(self.user.profile.balance, Decimal('90.00'))
        self.assertEqual(self.user.total_wager, Decimal('10.00'))

    def test_update_user_balance_for_win(self):
        """Test that _update_user_balance_for_win correctly updates the user's balance."""
        payout = Decimal('50.00')
        result = self.slot_service._update_user_balance_for_win(self.user, payout)
        
        # Check that the balance was updated
        self.assertTrue(result)
        self.assertEqual(self.user.profile.balance, Decimal('150.00'))
        self.assertEqual(self.user.total_won, Decimal('50.00'))

    def test_create_spin_record(self):
        """Test that _create_spin_record creates a new spin record."""
        bet_amount = Decimal('10.00')
        payout = Decimal('20.00')
        result = {0: [0, 1, 2], 1: [0, 1, 2], 2: [0, 1, 2]}
        win_data = {1: ['star', [0, 1, 2]]}
        
        spin = self.slot_service._create_spin_record(self.user, bet_amount, payout, result, win_data)
        
        # Check that the spin was created
        self.assertIsNotNone(spin)
        self.assertEqual(spin.user, self.user)
        self.assertEqual(spin.bet_amount, bet_amount)
        self.assertEqual(spin.payout, payout)
        self.assertEqual(spin.result, result)
        self.assertEqual(spin.win_data, win_data)

    @patch('slots.services.ReelService.generate_spin')
    @patch('slots.services.ReelService.check_wins')
    @patch('slots.services.ReelService.calculate_payout')
    def test_play_spin_no_win(self, mock_calculate_payout, mock_check_wins, mock_generate_spin):
        """Test playing a spin with no win."""
        # Mock the dependencies
        mock_generate_spin.return_value = {0: [0, 1, 2], 1: [1, 2, 0], 2: [2, 0, 1], 3: [0, 1, 2], 4: [1, 2, 0]}
        mock_check_wins.return_value = None
        mock_calculate_payout.return_value = Decimal('0.00')

        # Play a spin
        bet_amount = Decimal('10.00')
        result = self.slot_service.play_spin(self.user, bet_amount)

        # Check the result
        self.assertTrue(result['success'])
        self.assertEqual(result['payout'], Decimal('0.00'))
        self.assertEqual(result['current_balance'], float(Decimal('90.00')))
        self.assertIn('message', result)  # Should include a "you lost" message

        # Check that mock methods were called
        mock_generate_spin.assert_called_once()
        mock_check_wins.assert_called_once()
        mock_calculate_payout.assert_called_once_with(None, bet_amount)

    @patch('slots.services.ReelService.generate_spin')
    @patch('slots.services.ReelService.check_wins')
    @patch('slots.services.ReelService.calculate_payout')
    def test_play_spin_with_win(self, mock_calculate_payout, mock_check_wins, mock_generate_spin):
        """Test playing a spin with a win."""
        # Mock the dependencies
        win_data = {1: ['star', [0, 1, 2]]}
        mock_generate_spin.return_value = {0: [0, 1, 2], 1: [0, 1, 2], 2: [0, 1, 2], 3: [3, 4, 0], 4: [3, 4, 0]}
        mock_check_wins.return_value = win_data
        mock_calculate_payout.return_value = Decimal('60.00')

        # Play a spin
        bet_amount = Decimal('10.00')
        result = self.slot_service.play_spin(self.user, bet_amount)

        # Check the result
        self.assertTrue(result['success'])
        self.assertEqual(result['payout'], Decimal('60.00'))
        self.assertEqual(result['current_balance'], float(Decimal('150.00')))
        self.assertEqual(result['win_data'], win_data)

        # Check that mock methods were called
        mock_generate_spin.assert_called_once()
        mock_check_wins.assert_called_once()
        mock_calculate_payout.assert_called_once_with(win_data, bet_amount)

    def test_play_spin_insufficient_balance(self):
        """Test playing a spin with insufficient balance."""
        # Set user balance to a low amount
        self.user.profile.balance = Decimal('5.00')

        # Play a spin with a bet amount higher than the balance
        bet_amount = Decimal('10.00')
        result = self.slot_service.play_spin(self.user, bet_amount)

        # Check that the spin was not successful
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], 'Insufficient balance')


class SpinSerializerTestCase(TestCase):
    """Tests for the SpinSerializer"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        
        # Create a spin
        self.spin_data = {
            'user': self.user,
            'bet_amount': Decimal('10.00'),
            'payout': Decimal('20.00'),
            'result': {0: [0, 1, 2], 1: [0, 1, 2], 2: [0, 1, 2]},
            'win_data': {1: ['star', [0, 1, 2]]}
        }
        self.spin = Spin.objects.create(**self.spin_data)
        
    def test_spin_serializer(self):
        """Test that SpinSerializer correctly serializes a Spin object."""
        serializer = SpinSerializer(self.spin)
        data = serializer.data
        
        self.assertEqual(str(data['id']), str(self.spin.id))
        self.assertEqual(data['user'], self.user.id)
        self.assertEqual(data['bet_amount'], '10.00')
        self.assertEqual(data['payout'], '20.00')
        self.assertEqual(data['result'], self.spin_data['result'])
        self.assertEqual(data['win_data'], self.spin_data['win_data'])


class SpinRequestSerializerTestCase(TestCase):
    """Tests for the SpinRequestSerializer"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        # Set balance
        self.user.balance = Decimal('100.00')
        self.user.save()
        
    def test_valid_bet_amount(self):
        """Test that SpinRequestSerializer validates bet_amount correctly."""
        # Valid bet amount
        data = {'bet_amount': '10.00'}
        serializer = SpinRequestSerializer(data=data, context={'request': MagicMock(user=self.user)})
        self.assertTrue(serializer.is_valid())
        
    def test_bet_amount_too_small(self):
        """Test that SpinRequestSerializer rejects bet_amount below minimum."""
        # Bet amount too small
        data = {'bet_amount': '0.00'}
        serializer = SpinRequestSerializer(data=data, context={'request': MagicMock(user=self.user)})
        self.assertFalse(serializer.is_valid())
        
    def test_bet_amount_too_large(self):
        """Test that SpinRequestSerializer rejects bet_amount above maximum."""
        # Bet amount too large
        data = {'bet_amount': '2000.00'}
        serializer = SpinRequestSerializer(data=data, context={'request': MagicMock(user=self.user)})
        self.assertFalse(serializer.is_valid())


class ApiTests(APITestCase):
    """Tests for the API endpoints"""
    
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        
        # Create mock profile
        self.user.profile = MockUserProfileModel(Decimal('100.00'))
        
        # Add balance, total_wager, and total_won attributes to user
        self.user.total_wager = Decimal('0.00')
        self.user.total_won = Decimal('0.00')
        self.user.save()
        
        # Create symbols
        Symbol.objects.create(name='star', payout_multiplier=2.0)
        Symbol.objects.create(name='heart', payout_multiplier=1.5)
        Symbol.objects.create(name='cherry', payout_multiplier=1.2)
        Symbol.objects.create(name='gem', payout_multiplier=3.0)
        Symbol.objects.create(name='citrus', payout_multiplier=1.0)
        
        # Set up client
        self.client = APIClient()
        
        # Get token for authentication
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'email': 'test@example.com', 'password': 'testpass123'})
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        
    @patch('slots.services.SlotMachineService.play_spin')
    def test_spin_endpoint(self, mock_play_spin):
        """Test the spin endpoint."""
        # Mock the play_spin method
        mock_response = {
            'success': True,
            'spin_id': '12345',
            'result': {0: [0, 1, 2], 1: [0, 1, 2], 2: [0, 1, 2]},
            'win_data': {1: ['star', [0, 1, 2]]},
            'payout': Decimal('60.00'),
            'current_balance': float(Decimal('150.00'))
        }
        mock_play_spin.return_value = mock_response
        
        # Make request
        url = reverse('spin-spin')
        data = {'bet_amount': '10.00'}
        response = self.client.post(url, data)
        
        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, mock_response)
        
        # Check that play_spin was called with correct arguments
        mock_play_spin.assert_called_once_with(self.user, Decimal('10.00'))
        
    def test_spin_history_endpoint(self):
        """Test the spin history endpoint."""
        # Create some spins
        for i in range(3):
            Spin.objects.create(
                user=self.user,
                bet_amount=Decimal('10.00'),
                payout=Decimal(i * 10),
                result={0: [0, 1, 2], 1: [0, 1, 2], 2: [0, 1, 2]},
                win_data={1: ['star', [0, 1, 2]]} if i > 0 else None
            )
            
        # Make request
        url = reverse('spin-history')
        response = self.client.get(url)
        
        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        
    def test_symbol_list_endpoint(self):
        """Test the symbol list endpoint."""
        # Make request
        url = reverse('symbol-list')
        response = self.client.get(url)
        
        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)
        
    def test_frontend_mapping_endpoint(self):
        """Test the frontend mapping endpoint."""
        # Make request
        url = reverse('symbol-frontend-mapping')
        response = self.client.get(url)
        
        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('backend_to_frontend', response.data)
        self.assertIn('frontend_to_backend', response.data)
