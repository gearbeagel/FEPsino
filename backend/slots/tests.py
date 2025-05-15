from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from unittest.mock import patch, MagicMock
from .models import Symbol, Spin
from .services import ReelService, SlotMachineService

User = get_user_model()


class ReelServiceTestCase(TestCase):
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
        result = self.reel_service.generate_spin()

        # Check that result has 5 reels by default
        self.assertEqual(len(result), 5)

        # Check that each reel has 3 symbols by default
        for reel_num, symbols in result.items():
            self.assertEqual(len(symbols), 3)

        # Test with custom parameters
        result = self.reel_service.generate_spin(num_reels=3, visible_rows=2)
        self.assertEqual(len(result), 3)
        for reel_num, symbols in result.items():
            self.assertEqual(len(symbols), 2)

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

        # We should have a win in the first row (star symbols)
        self.assertIsNotNone(wins)
        self.assertIn(1, wins)  # Row 1 should have a win
        self.assertEqual(wins[1][0], 'star')  # The winning symbol should be 'star'

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

    def test_calculate_payout(self):
        """Test that calculate_payout correctly calculates the payout amount."""
        # Create a test win data
        win_data = {
            1: ['star', [0, 1, 2]],  # 3 stars in a row
            2: ['heart', [1, 2, 3]]  # 3 hearts in a row
        }

        bet_amount = Decimal('10.00')
        payout = self.reel_service.calculate_payout(win_data, bet_amount)

        # Expected payout: (10 * 3 * 2.0) + (10 * 3 * 1.5) = 60 + 45 = 105
        expected_payout = Decimal('105.00')
        self.assertEqual(payout, expected_payout)

        # Test with no win data
        payout = self.reel_service.calculate_payout(None, bet_amount)
        self.assertEqual(payout, Decimal('0.00'))

        # Test with non-existent symbol
        win_data = {
            1: ['nonexistent', [0, 1, 2]]
        }
        payout = self.reel_service.calculate_payout(win_data, bet_amount)
        # Should use default multiplier (1.0): 10 * 3 * 1.0 = 30
        expected_payout = Decimal('30.00')
        self.assertEqual(payout, expected_payout)

    def test_extract_horizontal_values(self):
        """Test that _extract_horizontal_values correctly extracts values from result dictionary."""
        result = {
            0: [0, 1, 2],
            1: [1, 2, 3],
            2: [2, 3, 4]
        }

        horizontal_values = self.reel_service._extract_horizontal_values(result)
        expected = [[0, 1, 2], [1, 2, 3], [2, 3, 4]]

        self.assertEqual(horizontal_values, expected)

    def test_transpose_matrix(self):
        """Test that _transpose_matrix correctly transposes a matrix."""
        matrix = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8]
        ]

        transposed = self.reel_service._transpose_matrix(matrix)
        expected = [
            [6, 3, 0],
            [7, 4, 1],
            [8, 5, 2]
        ]

        self.assertEqual(transposed, expected)

    def test_reverse_rows(self):
        """Test that _reverse_rows correctly reverses each row in a matrix."""
        matrix = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8]
        ]

        reversed_rows = self.reel_service._reverse_rows(matrix)
        expected = [
            [2, 1, 0],
            [5, 4, 3],
            [8, 7, 6]
        ]

        self.assertEqual(reversed_rows, expected)

    def test_find_winning_combinations(self):
        """Test that _find_winning_combinations correctly identifies winning combinations."""
        horizontal = [
            [0, 0, 0, 1, 2],
            [1, 1, 1, 0, 2],
            [2, 3, 4, 0, 1]
        ]

        wins = self.reel_service._find_winning_combinations(horizontal)

        self.assertIn(1, wins)  # Row 1 should have a win
        self.assertEqual(wins[1][0], 'star')  # The winning symbol should be 'star'
        self.assertEqual(wins[1][1], [0, 1, 2])  # The winning positions

        self.assertIn(2, wins)  # Row 2 should have a win
        self.assertEqual(wins[2][0], 'heart')  # The winning symbol should be 'heart'
        self.assertEqual(wins[2][1], [0, 1, 2])  # The winning positions

    def test_get_symbol_multiplier(self):
        """Test that _get_symbol_multiplier returns the correct multiplier for a symbol."""
        # Test with existing symbol
        multiplier = self.reel_service._get_symbol_multiplier('star')
        self.assertEqual(multiplier, Decimal('2.0'))

        # Test with non-existent symbol
        multiplier = self.reel_service._get_symbol_multiplier('nonexistent')
        self.assertEqual(multiplier, Decimal('1.0'))

    def test_calculate_win_payout(self):
        """Test that _calculate_win_payout correctly calculates payout for a single winning combination."""
        # Test with existing symbol
        payout = self.reel_service._calculate_win_payout('star', [0, 1, 2], Decimal('10.00'))
        expected_payout = Decimal('10.00') * 3 * Decimal('2.0')
        self.assertEqual(payout, expected_payout)

        # Test with non-existent symbol
        payout = self.reel_service._calculate_win_payout('nonexistent', [0, 1, 2], Decimal('10.00'))
        expected_payout = Decimal('10.00') * 3 * Decimal('1.0')
        self.assertEqual(payout, expected_payout)


class SlotMachineServiceTestCase(TestCase):
    def setUp(self):
        # Create test user with balance
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        # Add balance, total_wager, and total_won attributes to user
        self.user.balance = Decimal('100.00')
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

    def test_play_spin_insufficient_balance(self):
        """Test playing a spin with insufficient balance."""
        # Set user balance to a low amount
        self.user.balance = Decimal('5.00')
        self.user.save()

        # Play a spin with a bet amount higher than the balance
        bet_amount = Decimal('10.00')
        result = self.slot_service.play_spin(self.user, bet_amount)

        # Check that the spin was not successful
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], 'Insufficient balance')

        # Check that the user's balance was not changed
        self.user.refresh_from_db()
        self.assertEqual(self.user.balance, Decimal('5.00'))

    @patch('slots.services.ReelService.generate_spin')
    @patch('slots.services.ReelService.check_wins')
    @patch('slots.services.ReelService.calculate_payout')
    @patch('slots.services.Spin.objects.create')
    def test_create_spin_record(self, mock_spin_create, mock_calculate_payout, mock_check_wins, mock_generate_spin):
        """Test that _create_spin_record correctly creates a spin record."""
        # Mock the dependencies
        mock_generate_spin.return_value = {0: [0, 1, 2], 1: [0, 1, 2], 2: [0, 1, 2], 3: [3, 4, 0], 4: [3, 4, 0]}
        mock_check_wins.return_value = {1: ['star', [0, 1, 2]]}
        mock_calculate_payout.return_value = Decimal('60.00')

        mock_spin = MagicMock()
        mock_spin.id = 'test-uuid'
        mock_spin_create.return_value = mock_spin

        # Call _create_spin_record directly
        bet_amount = Decimal('10.00')
        payout = Decimal('60.00')
        result = {0: [0, 1, 2], 1: [0, 1, 2], 2: [0, 1, 2], 3: [3, 4, 0], 4: [3, 4, 0]}
        win_data = {1: ['star', [0, 1, 2]]}

        spin = self.slot_service._create_spin_record(self.user, bet_amount, payout, result, win_data)

        # Check that Spin.objects.create was called with the correct arguments
        mock_spin_create.assert_called_once_with(
            user=self.user,
            bet_amount=bet_amount,
            payout=payout,
            result=result,
            win_data=win_data
        )

        # Check that the returned spin is the mock_spin
        self.assertEqual(spin, mock_spin)

    def test_longest_seq_empty_input(self):
        """Test that longest_seq handles empty input correctly."""
        longest = self.slot_service.reel_service.longest_seq([])
        self.assertEqual(longest, [])

    def test_longest_seq_single_element(self):
        """Test that longest_seq handles single element input correctly."""
        longest = self.slot_service.reel_service.longest_seq([5])
        self.assertEqual(longest, [])

