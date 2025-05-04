import os
import unittest
from decimal import Decimal
from unittest import TestCase
from unittest.mock import patch, MagicMock

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

from rest_framework import serializers
from .game_logic import DiceGameLogic, GameContext
from .services import DiceGameService, CoinService
from .dice import Cube, Octahedron, Dodecahedron
from .serializers import StartDiceGameSerializer


class TestDice(unittest.TestCase):

    def test_cube_roll(self):
        cube = Cube()
        result = cube.roll()
        self.assertIn(result, range(1, 7))

    def test_octahedron_roll(self):
        octahedron = Octahedron()
        result = octahedron.roll()
        self.assertIn(result, range(1, 9))

    def test_dodecahedron_roll(self):
        dodecahedron = Dodecahedron()
        result = dodecahedron.roll()
        self.assertIn(result, range(1, 13))


class TestDiceGameLogic(unittest.TestCase):

    def setUp(self):
        self.mock_fig1 = MagicMock(spec=Cube)
        self.mock_fig2 = MagicMock(spec=Octahedron)
        self.mock_fig1.faces = 6
        self.mock_fig2.faces = 8

        self.factories = {
            6: MagicMock(create_figure=MagicMock(return_value=self.mock_fig1)),
            8: MagicMock(create_figure=MagicMock(return_value=self.mock_fig2)),
            12: MagicMock(create_figure=MagicMock(return_value=MagicMock(faces=12)))
        }

    def test_exact_guess_payout(self):
        self.mock_fig1.roll.return_value = 3
        self.mock_fig2.roll.return_value = 4
        logic = DiceGameLogic(self.factories, 100)
        result = logic.start_game(6, 8, bet=10, guessed_number=7)

        expected_multiplier = (6 + 8) / 10 + 1
        self.assertEqual(result['payout'], int(10 * expected_multiplier))
        self.assertEqual(result['total'], 7)

    def test_near_miss_payout(self):
        self.mock_fig1.roll.return_value = 3
        self.mock_fig2.roll.return_value = 4
        logic = DiceGameLogic(self.factories, 100)
        result = logic.start_game(6, 8, bet=10, guessed_number=6)

        expected_multiplier = (6 + 8) / 10
        self.assertEqual(result['payout'], int(10 * expected_multiplier))
        self.assertEqual(result['total'], 7)

    def test_total_miss_zero_payout(self):
        self.mock_fig1.roll.return_value = 1
        self.mock_fig2.roll.return_value = 2
        logic = DiceGameLogic(self.factories, 100)
        result = logic.start_game(6, 8, bet=10, guessed_number=10)

        self.assertEqual(result['payout'], 0)
        self.assertEqual(result['total'], 3)


class TestDiceGameService(unittest.TestCase):

    @patch('dice.services.transaction.atomic')
    @patch('dice.services.get_figure_factories')
    @patch('dice.services.DiceGameService.save_game_to_db')
    def test_execute_game_flow_win(self, mock_save_game, mock_get_factories, mock_atomic):
        user = MagicMock()
        user.profile.balance = Decimal('100.00')
        user.profile.save = MagicMock()

        factories = {
            3: MagicMock(),
            6: MagicMock(),
            8: MagicMock(),
            12: MagicMock()
        }

        mock_dice = MagicMock()
        mock_dice.roll.return_value = 3

        for factory in factories.values():
            factory.create_figure.return_value = mock_dice
        mock_get_factories.return_value = factories
        data = {
            'bet': 10,
            'choice1': 6,
            'choice2': 6,
            'guessed_number': 6
        }
        with patch('dice.game_logic.DiceGameLogic.start_game') as mock_start_game:
            mock_start_game.return_value = {
                'rolls': (3, 3),
                'total': 6,
                'payout': 20
            }

            result = DiceGameService.execute_game_flow(user, data)
            self.assertEqual(result['total'], 6)
            self.assertEqual(result['payout'], 20)
            user.profile.save.assert_called()
            mock_save_game.assert_called_once_with(user, data, result)

    @patch('dice.services.transaction.atomic')
    @patch('dice.services.get_figure_factories')
    @patch('dice.services.DiceGameService.save_game_to_db')
    def test_execute_game_flow_loss(self, mock_save_game, mock_get_factories, mock_atomic):
        user = MagicMock()
        user.profile.balance = Decimal('100.00')
        user.profile.save = MagicMock()

        factories = {
            6: MagicMock(),
            8: MagicMock(),
            12: MagicMock()
        }

        mock_dice = MagicMock()
        mock_dice.roll.return_value = 2
        for factory in factories.values():
            factory.create_figure.return_value = mock_dice
        mock_get_factories.return_value = factories

        data = {
            'bet': 10,
            'choice1': 6,
            'choice2': 6,
            'guessed_number': 7
        }
        with patch('dice.game_logic.DiceGameLogic.start_game') as mock_start_game:
            mock_start_game.return_value = {
                'rolls': (2, 2),
                'total': 4,
                'payout': 0
            }
            result = DiceGameService.execute_game_flow(user, data)
            self.assertEqual(result['total'], 4)
            self.assertEqual(result['payout'], 0)
            user.profile.save.assert_called()
            mock_save_game.assert_called_once_with(user, data, result)


class TestDiceGameServiceEdgeCases(unittest.TestCase):

    def test_insufficient_balance(self):
        user = MagicMock()
        user.profile.balance = Decimal('5.00')
        data = {'bet': 10, 'choice1': 6, 'choice2': 6, 'guessed_number': 7}
        with self.assertRaises(ValueError) as context:
            CoinService.check_user_coins(user, Decimal('10.00'))
        self.assertEqual(str(context.exception), "Not enough coins!")

    def test_guessed_number_less_than_two(self):
        data = {'bet': 10, 'choice1': 6, 'choice2': 6, 'guessed_number': 1}
        with self.assertRaises(serializers.ValidationError) as context:
            StartDiceGameSerializer(data=data).is_valid(raise_exception=True)
        self.assertIn("guessed_number", context.exception.detail)

    def test_guessed_number_greater_than_max(self):
        data = {'bet': 10, 'choice1': 6, 'choice2': 6, 'guessed_number': 13}
        with self.assertRaises(serializers.ValidationError) as context:
            StartDiceGameSerializer(data=data).is_valid(raise_exception=True)
        self.assertIn("guessed_number", context.exception.detail)

    def test_invalid_choice_value(self):
        data = {'bet': 10, 'choice1': 6, 'choice2': 7, 'guessed_number': 10}
        if 7 not in StartDiceGameSerializer.VALID_DICE_CHOICES:
            with self.assertRaises(serializers.ValidationError) as context:
                StartDiceGameSerializer(data=data).is_valid(raise_exception=True)
            self.assertIn("choice2", context.exception.detail)

    def test_invalid_bet_value(self):
        data = {'bet': 0, 'choice1': 6, 'choice2': 6, 'guessed_number': 7}
        with self.assertRaises(serializers.ValidationError) as context:
            StartDiceGameSerializer(data=data).is_valid(raise_exception=True)
        self.assertIn("bet", context.exception.detail)

    def test_negative_bet(self):
        data = {'bet': -5, 'choice1': 12, 'choice2': 6, 'guessed_number': 7}
        serializer = StartDiceGameSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('bet', serializer.errors)

    def test_non_integer_choice(self):
        data = {'bet': 10, 'choice1': 'six', 'choice2': 6, 'guessed_number': 7}
        serializer = StartDiceGameSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('choice1', serializer.errors)

    def test_missing_required_fields(self):
        serializer = StartDiceGameSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertIn('bet', serializer.errors)
        self.assertIn('choice1', serializer.errors)
        self.assertIn('choice2', serializer.errors)
        self.assertIn('guessed_number', serializer.errors)


class TestCoinService(TestCase):
    def test_check_user_coins_insufficient(self):
        user = MagicMock()
        user.profile.balance = Decimal('10.00')

        with self.assertRaises(ValueError):
            CoinService.check_user_coins(user, Decimal('20.00'))

    def test_check_user_coins_exact_balance(self):
        user = MagicMock()
        user.profile.balance = Decimal('50.00')

        try:
            CoinService.check_user_coins(user, Decimal('50.00'))
        except ValueError:
            self.fail("check_user_coins raised ValueError unexpectedly with exact balance")

    def test_update_balance_zero_payout(self):
        user = MagicMock()
        user.profile.balance = Decimal('100.00')
        user.profile.save = MagicMock()

        CoinService.update_balance(user, Decimal('0.00'))
        self.assertEqual(user.profile.balance, Decimal('100.00'))
        user.profile.save.assert_called_once()

    def test_update_balance_large_payout(self):
        user = MagicMock()
        user.profile.balance = Decimal('100.00')
        user.profile.save = MagicMock()

        CoinService.update_balance(user, Decimal('1000000.00'))
        self.assertEqual(user.profile.balance, Decimal('1000100.00'))
        user.profile.save.assert_called_once()


if __name__ == '__main__':
    unittest.main()