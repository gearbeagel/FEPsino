import unittest
from unittest.mock import MagicMock, patch
from decimal import Decimal


from .game_logic import BlackjackGame, Card
from .facade import BlackjackGameFacade, GameResult


class TestBlackjackGame(unittest.TestCase):
    """Tests for the BlackjackGame class."""

    def setUp(self):
        """Set up test environment before each test."""
        self.game = BlackjackGame()

    def test_card_creation(self):
        """Test that cards are created with correct rank and suit."""
        card = Card('A', '♥')
        self.assertEqual(card.rank, 'A')
        self.assertEqual(card.suit, '♥')
        self.assertEqual(str(card), 'A♥')

    def test_deck_creation(self):
        """Test that a deck contains 52 unique cards."""
        self.game.create_deck()

        self.assertEqual(len(self.game.deck), 52)

        card_strings = [str(card) for card in self.game.deck]
        self.assertEqual(len(card_strings), len(set(card_strings)))

    def test_deal_card(self):
        """Test dealing cards reduces deck size and returns a card."""
        self.game.create_deck()
        initial_deck_size = len(self.game.deck)
        card = self.game.deal_card()

        self.assertIsInstance(card, Card)
        self.assertEqual(len(self.game.deck), initial_deck_size - 1)

    def test_card_value_calculation(self):
        """Test calculation of card values."""
        self.assertEqual(self.game.card_value(Card('2', '♣')), 2)
        self.assertEqual(self.game.card_value(Card('10', '♠')), 10)
        self.assertEqual(self.game.card_value(Card('J', '♦')), 10)
        self.assertEqual(self.game.card_value(Card('Q', '♥')), 10)
        self.assertEqual(self.game.card_value(Card('K', '♣')), 10)
        self.assertEqual(self.game.card_value(Card('A', '♠')), 11)

    def test_hand_score_no_aces(self):
        """Test calculation of hand score without aces."""
        hand = [Card('10', '♥'), Card('K', '♣')]
        self.assertEqual(self.game.get_hand_score(hand), 20)

    def test_hand_score_with_aces(self):
        """Test calculation of hand score with aces that need to be adjusted."""

        hand1 = [Card('A', '♠'), Card('10', '♦')]
        self.assertEqual(self.game.get_hand_score(hand1), 21)


        hand2 = [Card('A', '♥'), Card('A', '♣'), Card('9', '♠')]
        self.assertEqual(self.game.get_hand_score(hand2), 21)


        hand3 = [Card('10', '♠'), Card('6', '♥'), Card('A', '♦')]
        self.assertEqual(self.game.get_hand_score(hand3), 17)

    def test_start_game(self):
        """Test that starting a game deals correct initial cards."""
        self.game.start_game()
        self.assertEqual(len(self.game.player_hand), 2)
        self.assertEqual(len(self.game.dealer_hand), 2)
        self.assertFalse(self.game.game_over)

    def test_player_hit_bust(self):
        """Test player hit that results in bust."""

        self.game.player_hand = [Card('10', '♠'), Card('5', '♥'), Card('5', '♦')]


        self.game.deck = [Card('K', '♣')]

        result = self.game.player_hit()

        self.assertTrue("Bust" in result)
        self.assertTrue(self.game.game_over)
        self.assertEqual(len(self.game.player_hand), 4)

    def test_player_hit_blackjack(self):
        """Test player hit that results in blackjack (21)."""

        self.game.player_hand = [Card('10', '♥'), Card('10', '♦')]


        self.game.deck = [Card('A', '♠')]

        result = self.game.player_hit()

        self.assertTrue("Blackjack" in result)
        self.assertTrue(self.game.game_over)

    def test_dealer_play_dealer_busts(self):
        """Test dealer play that results in dealer bust."""

        self.game.player_hand = [Card('10', '♥'), Card('8', '♣')]


        self.game.dealer_hand = [Card('10', '♠'), Card('6', '♦')]


        self.game.deck = [Card('K', '♥')]

        result = self.game.dealer_play()

        self.assertTrue("Dealer busts" in result)
        self.assertTrue(self.game.game_over)

    def test_dealer_play_dealer_wins(self):
        """Test dealer play that results in dealer win."""

        self.game.player_hand = [Card('10', '♦'), Card('5', '♠')]


        self.game.dealer_hand = [Card('10', '♥'), Card('6', '♣')]


        self.game.deck = [Card('A', '♦')]

        result = self.game.dealer_play()

        self.assertTrue("Dealer wins" in result)
        self.assertTrue(self.game.game_over)

    def test_game_state_during_game(self):
        """Test game state representation during game."""

        self.game.player_hand = [Card('J', '♠'), Card('7', '♦')]
        self.game.dealer_hand = [Card('A', '♥'), Card('4', '♣')]
        self.game.game_over = False

        state = self.game.get_game_state()


        self.assertEqual(len(state['dealer_hand']), 1)
        self.assertEqual(state['dealer_score'], 11)
        self.assertEqual(state['player_score'], 17)
        self.assertFalse(state['game_over'])


class TestBlackjackGameFacade(unittest.TestCase):
    """Tests for the BlackjackGameFacade class."""

    def setUp(self):
        """Set up test environment before each test."""
        self.user_mock = MagicMock()
        self.user_mock.profile.balance = Decimal('1000.00')
        self.facade = BlackjackGameFacade(self.user_mock)
        self.session = {}

    @patch('blackjack.facade.GameStateSerializer')
    def test_get_game_state_new_game(self, mock_serializer):
        """Test retrieving game state when no game exists."""
        mock_serializer().is_valid.return_value = True

        result = self.facade.get_game_state(self.session)

        self.assertTrue('game_state' in result)
        self.assertEqual(result['balance'], Decimal('1000.00'))
        self.assertEqual(result['bet'], 0)

    @patch('blackjack.facade.GameStateSerializer')
    @patch('blackjack.facade.BetSerializer')
    def test_start_new_game_with_bet(self, mock_bet_serializer, mock_game_serializer):
        """Test starting a new game with a valid bet."""
        mock_bet_serializer().is_valid.return_value = True
        mock_bet_serializer().validated_data = {'amount': 100}
        mock_game_serializer().is_valid.return_value = True

        result = self.facade.start_new_game_with_bet(self.session, 100)

        self.assertTrue('game_state' in result)
        self.assertEqual(self.user_mock.profile.deduct_balance.call_count, 1)
        self.assertEqual(self.session['bet'], 100)

    @patch('blackjack.facade.GameStateSerializer')
    def test_player_hit_during_game(self, mock_serializer):
        """Test player hitting during an active game."""

        self.session['game'] = {'game_over': False}
        self.session['bet'] = 50

        mock_serializer().is_valid.return_value = True

        with patch.object(BlackjackGame, 'player_hit', return_value=None):
            with patch.object(self.facade, '_restore_game_from_session'):
                with patch.object(self.facade, '_save_game_to_session'):
                    result = self.facade.player_hit(self.session)

                    self.assertTrue('game_state' in result)
                    self.assertEqual(result['bet'], 50)



    @patch('blackjack.facade.GameHistory.objects.create')
    def test_save_game_history(self, mock_create):
        """Test saving game history after game completion."""
        from .facade import GameHistory


        self.session['bet'] = 100

        game_mock = MagicMock()
        game_mock.player_hand = [Card('10', '♠'), Card('J', '♥')]
        game_mock.dealer_hand = [Card('9', '♦'), Card('8', '♣')]
        game_mock.get_hand_score.side_effect = [20, 17]


        self.facade._save_game_history(self.session, game_mock, GameHistory.OUTCOME_WIN)


        mock_create.assert_called_once()
        call_kwargs = mock_create.call_args[1]
        self.assertEqual(call_kwargs['user'], self.user_mock)
        self.assertEqual(call_kwargs['bet_amount'], 100)
        self.assertEqual(call_kwargs['outcome'], GameHistory.OUTCOME_WIN)


if __name__ == '__main__':
    unittest.main()