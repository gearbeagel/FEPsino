from .game_logic import BlackjackGame, Card
from .serializers import GameStateSerializer, BetSerializer, CardSerializer
from .models import GameHistory
from rest_framework.exceptions import ValidationError
from user.models import User
import json


class GameResult:
    """
    An object representing the result of a game action.
    Encapsulates game state, balance, bet, and optional message.
    """

    def __init__(self, game_state, balance, bet, message=None):
        self.game_state = game_state
        self.balance = balance
        self.bet = bet
        self.message = message

    def to_dict(self):
        """
        Converts the result to a dictionary for API response.
        """
        result = {
            'game_state': self.game_state,
            'balance': self.balance,
            'bet': self.bet
        }
        if self.message:
            result['message'] = self.message
        return result


class BlackjackGameFacade:
    """
    Facade pattern that provides a simplified interface to the BlackjackGame.
    """

    def __init__(self, user):
        self.user = user
        self.user.refresh_from_db()

    def get_current_balance(self):
        """
        Returns the current coin balance of the user.
        """
        self.user.refresh_from_db()
        return self.user.coin_balance

    def get_game_state(self, session):
        """
        Retrieves or initializes the game state from session.
        """
        game_state = session.get('game')
        bet = session.get('bet', 0)

        if not game_state:
            game_state = self._initialize_new_game(session)
        else:
            serializer = GameStateSerializer(data=game_state)
            if not serializer.is_valid():
                game_state = self._initialize_new_game(session)

        bet_serializer = BetSerializer(data={'amount': bet})
        if not bet_serializer.is_valid():
            session['bet'] = 0
            bet = 0

        return GameResult(
            game_state,
            self.get_current_balance(),
            bet
        ).to_dict()

    def _initialize_new_game(self, session):
        """
        Creates a new game instance with initial dealer card.
        """
        game = BlackjackGame()
        game.create_deck()
        game.dealer_hand = [game.deal_card()]

        game_state = game.get_game_state()

        serializer = GameStateSerializer(data=game_state)
        if serializer.is_valid():
            session['game'] = game_state
            return session['game']
        else:
            raise ValidationError("Failed to create a valid game state")

    def start_new_game(self, session):
        """
        Resets the game state and returns a fresh game state.
        """
        game_state = session.get('game')

        if game_state and not game_state.get('game_over', True):
            return GameResult(
                game_state,
                self.get_current_balance(),
                session.get('bet', 0),
                "Cannot start a new game while current game is in progress. Please finish the current game first."
            ).to_dict()

        new_game_state = self._initialize_new_game(session)
        session['bet'] = 0

        return GameResult(
            new_game_state,
            self.get_current_balance(),
            0,
            "New game started!"
        ).to_dict()

    def deal_cards(self, session):
        """
        Deals initial cards to player and dealer at the start of a game.
        """
        if 'game' in session and session['game'].get('game_over', False):
            return GameResult(
                session['game'],
                self.get_current_balance(),
                session.get('bet', 0),
                "Game is over. Please start a new game."
            ).to_dict()

        if 'game' not in session:
            game = self._create_new_game_instance()
        else:
            game = self._restore_game_from_session(session)

            if not game.game_over and not game.player_hand:
                for _ in range(2):
                    game.player_hand.append(game.deal_card())

                if len(game.dealer_hand) < 2:
                    game.dealer_hand.append(game.deal_card())

        self._save_game_to_session(session, game)

        return GameResult(
            session['game'],
            self.get_current_balance(),
            session.get('bet', 0)
        ).to_dict()

    def _create_new_game_instance(self):
        """
        Creates and initializes a new BlackjackGame instance.
        """
        game = BlackjackGame()
        game.create_deck()
        game.start_game()
        return game

    def _restore_game_from_session(self, session):
        """
        Restores a BlackjackGame instance from session data.
        """
        game_state = session['game']

        game_serializer = GameStateSerializer(data=game_state)
        if not game_serializer.is_valid():
            raise ValidationError("Invalid game state in session")

        game = BlackjackGame()

        if 'game_deck' in session:
            cards = []
            for card_data in session['game_deck']:
                card_serializer = CardSerializer(data=card_data)
                if card_serializer.is_valid():
                    cards.append(Card(**card_serializer.validated_data))
            game.deck = cards
        else:
            game.create_deck()

        player_cards = []
        for card_data in game_state['player_hand']:
            card_serializer = CardSerializer(data=card_data)
            if card_serializer.is_valid():
                player_cards.append(Card(**card_serializer.validated_data))
        game.player_hand = player_cards

        dealer_cards = []
        for card_data in game_state['dealer_hand']:
            if card_data.get('rank') == '?' and card_data.get('suit') == '?':
                continue
            card_serializer = CardSerializer(data=card_data)
            if card_serializer.is_valid():
                dealer_cards.append(Card(**card_serializer.validated_data))
        game.dealer_hand = dealer_cards

        game.game_over = game_state['game_over']

        return game

    def _save_game_to_session(self, session, game):
        """
        Saves the current game state to the session.
        """
        game_state = game.get_game_state()

        session['game_deck'] = [card.to_dict() for card in game.deck]

        serializer = GameStateSerializer(data=game_state)
        if serializer.is_valid():
            session['game'] = game_state
        else:
            raise ValidationError("Failed to create a valid game state")

    def player_hit(self, session):
        """
        Processes a player's request to hit (get another card).
        """
        if 'game' in session and session['game'].get('game_over', False):
            return {
                'message': "Game is over. Please start a new game."
            }

        game = self._restore_game_from_session(session)
        result = game.player_hit()

        if result and "Bust" in result:
            game.game_over = True
            self._save_game_to_session(session, game)
            self._save_game_history(session, game, GameHistory.OUTCOME_LOSS)
        else:
            self._save_game_to_session(session, game)

        return self._process_hit_result(session, result)

    def _process_hit_result(self, session, result):
        """
        Processes the result of a player hit action, updating balance if needed.
        """
        bet = session.get('bet', 0)

        if session['game'].get('game_over', False) and result and "Bust" in result:
            session['bet'] = 0

        return GameResult(
            session['game'],
            self.get_current_balance(),
            session.get('bet', 0),
            result
        ).to_dict()

    def player_stay(self, session):
        """
        Processes a player's decision to stay (no more cards).
        """
        if 'game' in session and session['game'].get('game_over', False):
            return {
                'message': "Game is over. Please start a new game."
            }

        game = self._restore_game_from_session(session)
        result = game.dealer_play()

        game.game_over = True
        self._save_game_to_session(session, game)

        outcome = None
        if "You win" in result:
            outcome = GameHistory.OUTCOME_WIN
        elif "tie" in result.lower():
            outcome = GameHistory.OUTCOME_TIE
        else:
            outcome = GameHistory.OUTCOME_LOSS

        self._save_game_history(session, game, outcome)

        return self._process_stay_result(session, result, outcome)

    def _process_stay_result(self, session, result, outcome):
        """
        Processes the result after a player stays, updating balance based on outcome.
        """
        bet = session.get('bet', 0)

        if outcome == GameHistory.OUTCOME_WIN:
            self._update_balance(bet * 2)
        elif outcome == GameHistory.OUTCOME_TIE:
            self._update_balance(bet)

        session['bet'] = 0

        return GameResult(
            session['game'],
            self.get_current_balance(),
            0,  # Bet is now 0
            result
        ).to_dict()

    def _save_game_history(self, session, game, outcome):
        """
        Save the game result to the GameHistory model.
        """
        bet = session.get('bet', 0)
        if bet == 0:
            return

        balance_before = self.get_current_balance()

        if outcome == GameHistory.OUTCOME_WIN:
            balance_change = bet
        elif outcome == GameHistory.OUTCOME_LOSS:
            balance_change = -bet
        else:  # Tie
            balance_change = 0

        if outcome == GameHistory.OUTCOME_WIN:
            balance_after = balance_before + (bet * 2)
        elif outcome == GameHistory.OUTCOME_TIE:
            balance_after = balance_before + bet
        else:
            balance_after = balance_before

        player_hand_str = json.dumps([{'rank': card.rank, 'suit': card.suit} for card in game.player_hand])
        dealer_hand_str = json.dumps([{'rank': card.rank, 'suit': card.suit} for card in game.dealer_hand])

        player_score = game.get_hand_score(game.player_hand)
        dealer_score = game.get_hand_score(game.dealer_hand)

        GameHistory.objects.create(
            user=self.user,
            bet_amount=bet,
            outcome=outcome,
            player_score=player_score,
            dealer_score=dealer_score,
            player_hand=player_hand_str,
            dealer_hand=dealer_hand_str,
            balance_change=balance_change,
            balance_before=balance_before,
            balance_after=balance_after
        )

    def place_bet(self, session, amount):
        """
        Places a bet of the specified amount and automatically deals cards.
        """
        if 'game' in session and not session['game'].get('game_over', False):
            game = self._restore_game_from_session(session)
            if game.player_hand:
                return GameResult(
                    session['game'],
                    self.get_current_balance(),
                    session.get('bet', 0),
                    "Cannot change bet during an active game."
                ).to_dict()


        if 'game' in session and session['game'].get('game_over', True):
            new_game_result = self.start_new_game(session)
            if 'message' in new_game_result and 'Cannot start a new game' in new_game_result['message']:
                return new_game_result


        bet_serializer = BetSerializer(data={'amount': amount})
        if not bet_serializer.is_valid():
            return GameResult(
                session.get('game'),
                self.get_current_balance(),
                session.get('bet', 0),
                "Invalid bet amount."
            ).to_dict()

        amount = bet_serializer.validated_data['amount']
        current_bet = session.get('bet', 0)

        if amount == 0:
            self._update_balance(current_bet)
            session['bet'] = 0
            return GameResult(
                session.get('game'),
                self.get_current_balance(),
                0,
                "Bet canceled."
            ).to_dict()
        elif self.get_current_balance() >= amount:
            session['bet'] = current_bet + amount
            self._update_balance(-amount)
        else:
            return GameResult(
                session.get('game'),
                self.get_current_balance(),
                current_bet,
                "Insufficient balance for this bet."
            ).to_dict()


        deal_result = self.deal_cards(session)
        deal_result['message'] = "Bet placed and cards dealt."

        return deal_result

    def _update_balance(self, amount):
        """
        Updates the user's coin balance and saves the user model.
        """
        self.user.coin_balance += amount
        self.user.save(update_fields=['coin_balance'])