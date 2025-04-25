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

        # Check that the user's balance was updated correctly
        self.user.refresh_from_db()
        self.assertEqual(self.user.balance, Decimal('90.00'))
        self.assertEqual(self.user.total_wager, Decimal('10.00'))
        self.assertEqual(self.user.total_won, Decimal('0.00'))

        # Check the result
        self.assertTrue(result['success'])
        self.assertEqual(result['payout'], Decimal('0.00'))
        self.assertEqual(result['current_balance'], float(Decimal('90.00')))

    @patch('slots.services.ReelService.generate_spin')
    @patch('slots.services.ReelService.check_wins')
    @patch('slots.services.ReelService.calculate_payout')
    def test_play_spin_with_win(self, mock_calculate_payout, mock_check_wins, mock_generate_spin):
        """Test playing a spin with a win."""
        # Mock the dependencies
        mock_generate_spin.return_value = {0: [0, 1, 2], 1: [0, 1, 2], 2: [0, 1, 2], 3: [3, 4, 0], 4: [3, 4, 0]}
        mock_check_wins.return_value = {1: ['star', [0, 1, 2]]}
        mock_calculate_payout.return_value = Decimal('60.00')

        # Play a spin
        bet_amount = Decimal('10.00')
        result = self.slot_service.play_spin(self.user, bet_amount)

        # Check that the user's balance was updated correctly
        self.user.refresh_from_db()
        self.assertEqual(self.user.balance, Decimal('150.00'))  # 100 - 10 + 60 = 150
        self.assertEqual(self.user.total_wager, Decimal('10.00'))
        self.assertEqual(self.user.total_won, Decimal('60.00'))

        # Check the result
        self.assertTrue(result['success'])
        self.assertEqual(result['payout'], Decimal('60.00'))
        self.assertEqual(result['current_balance'], float(Decimal('150.00')))

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
