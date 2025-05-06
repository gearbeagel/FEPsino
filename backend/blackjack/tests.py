import unittest
from unittest.mock import Mock, patch
from .game_logic import BlackjackGame, Card
from .facade import BlackjackGameFacade


class TestBlackjackGameFacade(unittest.TestCase):
    """Test the BlackjackGameFacade class for correct interaction with the game logic."""

    def setUp(self):
        self.user_mock = Mock()
        self.facade = BlackjackGameFacade(self.user_mock)
        self.session = {}

    def test_get_game_state_new_game(self):
        """Test getting game state when no game is in progress."""
        result = self.facade.get_game_state(self.session)
        self.assertIn('game_state', result)
        self.assertIn('balance', result)
        self.assertEqual(result['bet'], 0)
        self.assertIn('game', self.session)

    def test_start_new_game_with_bet_success(self):
        """Test starting a new game with a bet when no game is in progress."""
        with patch.object(self.facade, 'get_current_balance', return_value=1000):
            with patch.object(self.facade, '_update_balance') as mock_update_balance:
                result = self.facade.start_new_game_with_bet(self.session, 100)

                self.assertIn('message', result)
                self.assertEqual(result['message'], "Bet placed and cards dealt.")
                self.assertEqual(result['bet'], 100)

                mock_update_balance.assert_called_once_with(-100)

                self.assertEqual(len(result['game_state']['player_hand']), 2)
                self.assertEqual(len(result['game_state']['dealer_hand']), 2)

    def test_start_new_game_with_bet_game_in_progress(self):
        """Test starting a new game with a bet when a game is already in progress."""

        self.session['game'] = {'game_over': False}
        self.session['bet'] = 100

        result = self.facade.start_new_game_with_bet(self.session, 200)
        self.assertIn('message', result)
        self.assertEqual(result['message'], "Cannot change bet during an active game.")

    def test_start_new_game_with_bet_insufficient_funds(self):
        """Test starting a new game with a bet with insufficient funds."""
        with patch.object(self.facade, 'get_current_balance', return_value=50):
            result = self.facade.start_new_game_with_bet(self.session, 100)
            self.assertIn('message', result)
            self.assertEqual(result['message'], "Insufficient balance for this bet.")

    def test_deal_cards_new_game(self):
        """Test dealing cards when starting a new game."""
        result = self.facade.deal_cards(self.session)
        self.assertEqual(len(result['game_state']['player_hand']), 2)
        self.assertGreaterEqual(len(result['game_state']['dealer_hand']), 2)

    def test_deal_cards_game_over(self):
        """Test dealing cards when the game is over."""
        self.session['game'] = {'game_over': True}
        result = self.facade.deal_cards(self.session)
        self.assertIn('message', result)
        self.assertEqual(result['message'], "Game is over. Please start a new game.")

    def test_player_hit_success(self):
        """Test player hitting when the game is in progress."""
        self.facade.deal_cards(self.session)

        game_mock = Mock()
        game_mock.player_hit.return_value = "Card dealt successfully."
        game_mock.get_game_state.return_value = {
            'player_hand': [{'rank': 'A', 'suit': 'H'}, {'rank': '5', 'suit': 'D'}, {'rank': '3', 'suit': 'C'}],
            'dealer_hand': [{'rank': 'K', 'suit': 'S'}, {'rank': '?', 'suit': '?'}],
            'player_score': 19,
            'dealer_score': 10,
            'game_over': False
        }

        serializer_mock = Mock()
        serializer_mock.is_valid.return_value = True

        with patch.object(self.facade, '_restore_game_from_session', return_value=game_mock), \
                patch('blackjack.facade.GameStateSerializer', return_value=serializer_mock):
            result = self.facade.player_hit(self.session)

            self.assertEqual(result['message'], "Card dealt successfully.")
            self.assertFalse(result['game_state']['game_over'])
            game_mock.player_hit.assert_called_once()

    def test_player_hit_bust(self):
        """Test player hitting resulting in bust."""
        self.facade.deal_cards(self.session)
        self.session['bet'] = 100

        game_mock = Mock()
        game_mock.player_hit.return_value = "Bust! You lose."
        game_mock.get_game_state.return_value = {
            'player_hand': [{'rank': '10', 'suit': 'H'}, {'rank': 'K', 'suit': 'D'}, {'rank': '5', 'suit': 'C'}],
            'dealer_hand': [{'rank': '7', 'suit': 'S'}, {'rank': '?', 'suit': '?'}],
            'player_score': 25,
            'dealer_score': 7,
            'game_over': True
        }

        serializer_mock = Mock()
        serializer_mock.is_valid.return_value = True

        with patch.object(self.facade, '_restore_game_from_session', return_value=game_mock), \
                patch.object(self.facade, '_save_game_history'), \
                patch('blackjack.facade.GameStateSerializer', return_value=serializer_mock):
            result = self.facade.player_hit(self.session)

            self.assertEqual(result['message'], "Bust! You lose.")
            self.assertTrue(result['game_state']['game_over'])
            self.assertEqual(result['bet'], 0)
            game_mock.player_hit.assert_called_once()
            self.facade._save_game_history.assert_called_once()

    def test_player_hit_game_over(self):
        """Test player hitting when the game is over."""
        self.session['game'] = {'game_over': True}

        result = self.facade.player_hit(self.session)
        self.assertIn('message', result)
        self.assertEqual(result['message'], "Game is over. Please start a new game.")

    def test_player_stay_player_wins(self):
        """Test player staying when the player wins."""
        self.facade.deal_cards(self.session)
        self.session['bet'] = 100

        initial_balance = self.facade.get_current_balance()

        game_mock = Mock()
        game_mock.dealer_play.return_value = "You win!"
        game_mock.get_game_state.return_value = {
            'player_hand': [{'rank': 'A', 'suit': 'H'}, {'rank': 'K', 'suit': 'D'}],
            'dealer_hand': [{'rank': '10', 'suit': 'S'}, {'rank': '8', 'suit': 'C'}],
            'player_score': 21,
            'dealer_score': 18,
            'game_over': True
        }
        game_mock.get_hand_score = lambda hand: 21 if hand == game_mock.player_hand else 18

        serializer_mock = Mock()
        serializer_mock.is_valid.return_value = True

        with patch.object(self.facade, '_restore_game_from_session', return_value=game_mock), \
                patch.object(self.facade, '_update_balance') as mock_update_balance, \
                patch.object(self.facade, '_save_game_history'), \
                patch('blackjack.facade.GameStateSerializer', return_value=serializer_mock):
            result = self.facade.player_stay(self.session)

            self.assertEqual(result['message'], "You win!")
            self.assertEqual(result['bet'], 0)
            self.assertTrue(result['game_state']['game_over'])

            mock_update_balance.assert_called_once_with(200)

            self.facade._save_game_history.assert_called_once()

    def test_player_stay_dealer_wins(self):
        """Test player staying when the dealer wins."""
        self.facade.deal_cards(self.session)
        self.session['bet'] = 100

        game_mock = Mock()
        game_mock.dealer_play.return_value = "Dealer wins!"
        game_mock.get_game_state.return_value = {
            'player_hand': [{'rank': 'J', 'suit': 'C'}, {'rank': '8', 'suit': 'D'}],
            'dealer_hand': [{'rank': 'K', 'suit': 'H'}, {'rank': 'Q', 'suit': 'S'}],
            'player_score': 18,
            'dealer_score': 20,
            'game_over': True
        }
        game_mock.get_hand_score = lambda hand: 18 if hand == game_mock.player_hand else 20

        serializer_mock = Mock()
        serializer_mock.is_valid.return_value = True

        with patch.object(self.facade, '_restore_game_from_session', return_value=game_mock), \
                patch.object(self.facade, '_save_game_history'), \
                patch('blackjack.facade.GameStateSerializer', return_value=serializer_mock):
            result = self.facade.player_stay(self.session)

            self.assertEqual(result['message'], "Dealer wins!")
            self.assertEqual(result['bet'], 0)
            self.assertTrue(result['game_state']['game_over'])

            self.facade._save_game_history.assert_called_once()

    def test_player_stay_tie(self):
        """Test player staying resulting in a tie."""
        self.facade.deal_cards(self.session)
        self.session['bet'] = 100

        game_mock = Mock()
        game_mock.dealer_play.return_value = "It's a tie!"
        game_mock.get_game_state.return_value = {
            'player_hand': [{'rank': '10', 'suit': 'H'}, {'rank': '7', 'suit': 'D'}],
            'dealer_hand': [{'rank': 'J', 'suit': 'S'}, {'rank': '7', 'suit': 'C'}],
            'player_score': 17,
            'dealer_score': 17,
            'game_over': True
        }
        game_mock.get_hand_score = lambda hand: 17

        serializer_mock = Mock()
        serializer_mock.is_valid.return_value = True

        with patch.object(self.facade, '_restore_game_from_session', return_value=game_mock), \
                patch.object(self.facade, '_update_balance') as mock_update_balance, \
                patch.object(self.facade, '_save_game_history'), \
                patch('blackjack.facade.GameStateSerializer', return_value=serializer_mock):
            result = self.facade.player_stay(self.session)

            self.assertEqual(result['message'], "It's a tie!")
            self.assertEqual(result['bet'], 0)
            self.assertTrue(result['game_state']['game_over'])

            mock_update_balance.assert_called_once_with(100)

            self.facade._save_game_history.assert_called_once()

    def test_player_stay_game_over(self):
        """Test player staying when the game is over."""
        self.session['game'] = {'game_over': True}

        result = self.facade.player_stay(self.session)
        self.assertIn('message', result)
        self.assertEqual(result['message'], "Game is over. Please start a new game.")

    def test_save_game_history(self):
        """Test saving game history when a game ends."""
        from .models import GameHistory

        self.facade.deal_cards(self.session)
        self.session['bet'] = 100

        game = BlackjackGame()
        game.player_hand = [Card('A', '♠'), Card('K', '♦')]  # 21
        game.dealer_hand = [Card('10', '♥'), Card('5', '♣')]  # 15

        with patch('blackjack.models.GameHistory.objects.create') as mock_create, \
                patch.object(self.facade, 'get_current_balance', return_value=1000):

            self.facade._save_game_history(self.session, game, GameHistory.OUTCOME_WIN)
            mock_create.assert_called_once()

            args, kwargs = mock_create.call_args
            self.assertEqual(kwargs['user'], self.user_mock)
            self.assertEqual(kwargs['bet_amount'], 100)
            self.assertEqual(kwargs['outcome'], GameHistory.OUTCOME_WIN)
            self.assertEqual(kwargs['player_score'], 21)
            self.assertEqual(kwargs['dealer_score'], 15)
            self.assertEqual(kwargs['balance_change'], 100)
            self.assertEqual(kwargs['balance_before'], 1000)
            self.assertEqual(kwargs['balance_after'], 1200)


if __name__ == '__main__':
    unittest.main()