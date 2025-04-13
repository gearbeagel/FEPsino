import unittest
from unittest.mock import Mock, patch
from .game_logic import BlackjackGame, Card
from .facade import BlackjackGameFacade


class TestCard(unittest.TestCase):
    """Test the Card class for correct initialization and string representation."""
    def test_card_creation(self):
        """Test card creation with rank and suit."""
        card = Card('A', '♥')
        self.assertEqual(card.rank, 'A')
        self.assertEqual(card.suit, '♥')

    def test_card_string_representation(self):
        """Test string representation of the card."""
        card = Card('10', '♠')
        self.assertEqual(str(card), '10♠')

    def test_card_to_dict(self):
        """Test conversion of card to dictionary."""
        card = Card('K', '♦')
        expected = {'rank': 'K', 'suit': '♦'}
        self.assertEqual(card.to_dict(), expected)


class TestBlackjackGame(unittest.TestCase):
    """Test the BlackjackGame class for game logic and functionality."""
    def setUp(self):

        self.game = BlackjackGame()

    def test_create_deck(self):
        """Test deck creation with 52 unique cards."""
        self.game.create_deck()
        self.assertEqual(len(self.game.deck), 52)

    def test_deal_card(self):
        """Test dealing a card from the deck."""
        self.game.create_deck()
        initial_deck_size = len(self.game.deck)
        card = self.game.deal_card()
        self.assertIsInstance(card, Card)
        self.assertEqual(len(self.game.deck), initial_deck_size - 1)

    def test_deal_card_empty_deck(self):
        """Test dealing a card when the deck is empty."""
        self.game.deck = []
        card = self.game.deal_card()
        self.assertIsInstance(card, Card)
        self.assertEqual(len(self.game.deck), 51)

    def test_card_value_regular(self):
        """Test card value for regular cards (2-10)."""
        card = Card('7', '♣')
        self.assertEqual(self.game.card_value(card), 7)

    def test_card_value_face_cards(self):
        """Test card value for face cards (J, Q, K)."""
        cards = [Card('J', '♥'), Card('Q', '♠'), Card('K', '♦')]
        for card in cards:
            self.assertEqual(self.game.card_value(card), 10)

    def test_card_value_ace(self):
        """Test card value for Ace (A)."""
        card = Card('A', '♣')
        self.assertEqual(self.game.card_value(card), 11)

    def test_calculate_hand_simple(self):
        """Test calculation of hand value without Aces."""
        hand = [Card('5', '♠'), Card('7', '♣')]
        self.assertEqual(self.game.calculate_hand(hand), 12)

    def test_calculate_hand_with_face_cards(self):
        """Test calculation with face cards."""
        hand = [Card('K', '♥'), Card('Q', '♦')]
        self.assertEqual(self.game.calculate_hand(hand), 20)

    def test_calculate_hand_with_aces_adjustment(self):
        """Test calculation with Aces."""
        hand = [Card('A', '♠'), Card('A', '♥'), Card('9', '♣')]
        self.assertEqual(self.game.calculate_hand(hand), 21)

    def test_player_hit_bust(self):
        """Test player hit resulting in bust."""

        self.game.player_hand = [Card('10', '♠'), Card('9', '♥')]
        self.game.deck = [Card('K', '♦')]  # Next card will cause bust

        result = self.game.player_hit()
        self.assertEqual(result, "Bust! You lose.")
        self.assertTrue(self.game.game_over)

    def test_player_hit_blackjack(self):
        """Test player hit resulting in blackjack."""
        self.game.player_hand = [Card('10', '♠'), Card('A', '♥')]
        self.game.deck = [Card('10', '♦')]

        result = self.game.player_hit()
        self.assertEqual(result, "Blackjack! 21 points.")

    def test_dealer_play_dealer_busts(self):

        """Test dealer play resulting in dealer bust."""
        self.game.player_hand = [Card('10', '♠'), Card('8', '♥')]  # 18
        self.game.dealer_hand = [Card('10', '♦'), Card('6', '♣')]  # 16
        self.game.deck = [Card('K', '♥')]  # Next card will cause dealer to bust

        result = self.game.dealer_play()
        self.assertEqual(result, "Dealer busts! You win!")
        self.assertTrue(self.game.game_over)

    def test_dealer_play_dealer_wins(self):

        """Test dealer play resulting in dealer win."""
        self.game.player_hand = [Card('10', '♠'), Card('5', '♥')]  # 15
        self.game.dealer_hand = [Card('10', '♦'), Card('7', '♣')]  # 17

        result = self.game.dealer_play()
        self.assertEqual(result, "Dealer wins!")
        self.assertTrue(self.game.game_over)

    def test_dealer_play_player_wins(self):
        """Test dealer play resulting in player win."""
        self.game.player_hand = [Card('10', '♠'), Card('9', '♥')]  # 19
        self.game.dealer_hand = [Card('10', '♦'), Card('7', '♣')]  # 17

        result = self.game.dealer_play()
        self.assertEqual(result, "You win!")
        self.assertTrue(self.game.game_over)

    def test_dealer_play_tie(self):
        """Test dealer play resulting in a tie."""
        self.game.player_hand = [Card('10', '♠'), Card('7', '♥')]  # 17
        self.game.dealer_hand = [Card('10', '♦'), Card('7', '♣')]  # 17

        result = self.game.dealer_play()
        self.assertEqual(result, "It's a tie!")
        self.assertTrue(self.game.game_over)


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

    def test_start_new_game_success(self):
        """Test starting a new game when no game is in progress."""
        result = self.facade.start_new_game(self.session)
        self.assertIn('message', result)
        self.assertEqual(result['message'], "New game started!")
        self.assertEqual(result['bet'], 0)

    def test_start_new_game_in_progress(self):
        """Test starting a new game when a game is already in progress."""
        self.session['game'] = {'game_over': False}
        self.session['bet'] = 100

        result = self.facade.start_new_game(self.session)
        self.assertIn('message', result)
        self.assertTrue("Cannot start a new game" in result['message'])

    def test_deal_cards_new_game(self):
        """Test dealing cards when starting a new game."""
        result = self.facade.deal_cards(self.session)
        self.assertEqual(len(result['game_state']['player_hand']), 2)
        self.assertGreaterEqual(len(result['game_state']['dealer_hand']), 1)

    def test_deal_cards_game_over(self):
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
            'player_hand': [{'rank': 'A', 'suit': 'H'}],
            'dealer_hand': [{'rank': 'K', 'suit': 'S'}],
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

    def test_player_stay_dealer_wins(self):
        """Test player staying when the dealer wins."""

        self.facade.deal_cards(self.session)
        self.session['bet'] = 100


        initial_balance = self.facade.get_current_balance()


        game_mock = Mock()
        game_mock.dealer_play.return_value = "Dealer wins!"
        game_mock.get_game_state.return_value = {
            'player_hand': [{'rank': 'J', 'suit': 'C'}, {'rank': '8', 'suit': 'D'}],
            'dealer_hand': [{'rank': 'K', 'suit': 'H'}, {'rank': 'Q', 'suit': 'S'}],
            'game_over': True
        }


        serializer_mock = Mock()
        serializer_mock.is_valid.return_value = True


        with patch.object(self.facade, '_restore_game_from_session', return_value=game_mock), \
                patch('blackjack.facade.GameStateSerializer', return_value=serializer_mock):

            result = self.facade.player_stay(self.session)


            self.assertEqual(result['message'], "Dealer wins!")
            self.assertEqual(result['bet'], 0)
            self.assertTrue(result['game_state']['game_over'])
            self.assertEqual(result['balance'], initial_balance)
            game_mock.dealer_play.assert_called_once()


    def test_place_bet_success(self):

        """Test placing a bet when the game is in progress."""
        self.facade.deal_cards(self.session)
        initial_balance = self.facade.get_current_balance()

        result = self.facade.place_bet(self.session, 100)
        self.assertEqual(result['balance'], initial_balance - 100)
        self.assertEqual(result['bet'], 100)
        self.assertEqual(result['message'], "Bet placed successfully.")

    def test_place_bet_insufficient_funds(self):
        """Test placing a bet with insufficient funds."""
        self.facade.deal_cards(self.session)
        large_amount = self.facade.get_current_balance() + 1000

        result = self.facade.place_bet(self.session, large_amount)
        self.assertEqual(result['bet'], 0)  # Bet should not change

    def test_place_bet_game_over(self):
        """Test placing a bet when the game is over."""
        self.session['game'] = {'game_over': True}

        result = self.facade.place_bet(self.session, 100)
        self.assertIn('message', result)
        self.assertTrue("game is over" in result['message'].lower())


if __name__ == '__main__':
    unittest.main()
    # Run the tests