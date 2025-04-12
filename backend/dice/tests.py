import os
import unittest
from unittest.mock import MagicMock, patch
from .game_logic import DiceGameLogic, GameContext
from .services import DiceGameService, CoinService
from .dice import Cube, Octahedron, Dodecahedron
from .serializers import StartDiceGameSerializer
from rest_framework import serializers

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")


class TestDice(unittest.TestCase):

    def test_cube_roll(self):
        cube = Cube()
        cube.faces = 6
        result = cube.roll()
        self.assertIn(result, range(1, 7))

    def test_octahedron_roll(self):
        octahedron = Octahedron()
        octahedron.faces = 8
        result = octahedron.roll()
        self.assertIn(result, range(1, 9))

    def test_dodecahedron_roll(self):
        dodecahedron = Dodecahedron()
        dodecahedron.faces = 12
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
        self.assertEqual(result['user_coins'], 90)


class TestDiceGameService(unittest.TestCase):

    @patch('dice.services.DiceGameModel.objects.create')
    @patch('dice.services.get_figure_factories')
    def test_execute_game_flow(self, mock_get_factories, mock_model_create):
        user = MagicMock()
        user.coin_balance = 100

        mock_fig = MagicMock()
        mock_fig.roll.side_effect = [2, 3]
        mock_fig.faces = 6

        factory = MagicMock()
        factory.create_figure.return_value = mock_fig
        mock_get_factories.return_value = {6: factory}

        data = {'bet': 10, 'choice1': 6, 'choice2': 6, 'guessed_number': 5}

        result = DiceGameService.execute_game_flow(user, data)

        self.assertEqual(result['total'], 5)
        mock_model_create.assert_called_once()
        user.save.assert_called_once()

    def test_deduct_and_update_balance(self):
        user = MagicMock()
        user.coin_balance = 100

        CoinService.deduct_bet(user, 10)
        self.assertEqual(user.coin_balance, 90)

        CoinService.update_balance(user, 15)
        self.assertEqual(user.coin_balance, 105)
        user.save.assert_called_once()


class TestDiceGameServiceEdgeCases(unittest.TestCase):

    @patch('dice.services.get_figure_factories')
    def test_insufficient_balance(self, mock_get_factories):
        user = MagicMock()
        user.coin_balance = 5

        data = {'bet': 10, 'choice1': 6, 'choice2': 6, 'guessed_number': 7}

        with self.assertRaises(ValueError) as context:
            DiceGameService.execute_game_flow(user, data)
        self.assertEqual(str(context.exception), "Not enough coins!")

    def test_guessed_number_less_than_two(self):
        user = MagicMock()
        user.coin_balance = 100

        data = {'bet': 10, 'choice1': 6, 'choice2': 6, 'guessed_number': 1}

        with self.assertRaises(serializers.ValidationError) as context:
            StartDiceGameSerializer(data=data).is_valid(raise_exception=True)
        self.assertIn("guessed_number", context.exception.detail)

    def test_guessed_number_greater_than_max(self):
        user = MagicMock()
        user.coin_balance = 100

        data = {'bet': 10, 'choice1': 6, 'choice2': 6, 'guessed_number': 13}

        with self.assertRaises(serializers.ValidationError) as context:
            StartDiceGameSerializer(data=data).is_valid(raise_exception=True)
        self.assertIn("guessed_number", context.exception.detail)

    def test_invalid_choice_value(self):
        user = MagicMock()
        user.coin_balance = 100

        data = {'bet': 10, 'choice1': 6, 'choice2': 7, 'guessed_number': 10}

        with self.assertRaises(serializers.ValidationError) as context:
            StartDiceGameSerializer(data=data).is_valid(raise_exception=True)
        self.assertIn("choice2", context.exception.detail)

    def test_invalid_bet_value(self):
        data = {'bet': 0, 'choice1': 6, 'choice2': 6, 'guessed_number': 7}
        with self.assertRaises(serializers.ValidationError) as context:
            StartDiceGameSerializer(data=data).is_valid(raise_exception=True)
        self.assertIn("bet", context.exception.detail)

    def test_non_integer_bet(self):
        data = {'bet': 10.5, 'choice1': 12, 'choice2': 6, 'guessed_number': 7}
        serializer = StartDiceGameSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('bet', serializer.errors)

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


class TestCoinService(unittest.TestCase):

    def test_check_user_coins_exact_balance(self):
        user = MagicMock()
        user.coin_balance = 50
        try:
            CoinService.check_user_coins(user, 50)
        except ValueError:
            self.fail("check_user_coins raised ValueError unexpectedly with exact balance")

    def test_deduct_bet_zero(self):
        user = MagicMock()
        user.coin_balance = 100
        CoinService.deduct_bet(user, 0)
        self.assertEqual(user.coin_balance, 100)

    def test_update_balance_zero_payout(self):
        user = MagicMock()
        user.coin_balance = 100
        CoinService.update_balance(user, 0)
        self.assertEqual(user.coin_balance, 100)
        user.save.assert_called_once()

    def test_update_balance_large_payout(self):
        user = MagicMock()
        user.coin_balance = 100
        CoinService.update_balance(user, 10**6)
        self.assertEqual(user.coin_balance, 100 + 10**6)
        user.save.assert_called_once()


if __name__ == '__main__':
    unittest.main()