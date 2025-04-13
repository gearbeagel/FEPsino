from .game_logic import BlackjackGame, Card
from .serializers import GameStateSerializer, BetSerializer, CardSerializer
from rest_framework.exceptions import ValidationError


# REFACTORING: Introduce Parameter Object
# REFACTORING: Extract Class
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
    Manages game state persistence in session and handles user profile interactions.
    Uses serializers for data validation.
    """

    def __init__(self, user):
        self.user = user
        # REFACTORING: Extract Mock Object - separating test code from production code
        self.profile = type('obj', (object,), {'balance': 1000, 'save': lambda: None})

    # REFACTORING: Replace Temporary Variable with Query
    # REFACTORING: Encapsulate Field
    def get_current_balance(self):
        """
        Returns the current balance of the user profile.
        """
        return self.profile.balance

    def get_game_state(self, session):
        """
        Retrieves or initializes the game state from session.
        Uses serializer to validate the game state.
        """
        game_state = session.get('game')
        bet = session.get('bet', 0)

        if not game_state:
            # REFACTORING: Extract Method - create a new helper method for initialization
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
        Ensures the game state is properly serialized.
        """
        # REFACTORING: Extract Method - improves readability by breaking down complex method
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
        Only allowed when no game is in progress or current game is over.
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
            # REFACTORING: Extract Method
            game = self._create_new_game_instance()
        else:
            # REFACTORING: Extract Method
            game = self._restore_game_from_session(session)

            # REFACTORING: Simplify Conditional Expression
            if not game.game_over and not game.player_hand:
                for _ in range(2):
                    game.player_hand.append(game.deal_card())

                if not game.dealer_hand:
                    game.dealer_hand.append(game.deal_card())

        # REFACTORING: Extract Method
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
        # REFACTORING: Extract Method
        game = BlackjackGame()
        game.create_deck()
        game.start_game()
        return game

    def _restore_game_from_session(self, session):
        """
        Restores a BlackjackGame instance from session data.
        Uses card serializer to validate card data.
        """
        # REFACTORING: Extract Method
        game_state = session['game']


        game_serializer = GameStateSerializer(data=game_state)
        if not game_serializer.is_valid():
            raise ValidationError("Invalid game state in session")

        game = BlackjackGame()

        # REFACTORING: Simplify Conditional Expression
        if 'deck' in game_state:

            cards = []
            for card_data in game_state['deck']:
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
        Validates the game state with serializer before saving.
        """
        # REFACTORING: Extract Method
        game_state = game.get_game_state()


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
            return GameResult(
                session['game'],
                self.get_current_balance(),
                session.get('bet', 0),
                "Game is over. Please start a new game."
            ).to_dict()

        # REFACTORING: Extract Method
        game = self._restore_game_from_session(session)

        result = game.player_hit()
        self._save_game_to_session(session, game)

        # REFACTORING: Extract Method
        return self._process_hit_result(session, result)

    def _process_hit_result(self, session, result):
        """
        Processes the result of a player hit action, updating balance if needed.
        """
        # REFACTORING: Extract Method
        if result == "Bust! You lose.":
            bet = session.get('bet', 0)
            self._update_balance(-bet)
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
            # REFACTORING: Introduce Parameter Object
            return GameResult(
                session['game'],
                self.get_current_balance(),
                session.get('bet', 0),
                "Game is over. Please start a new game."
            ).to_dict()

        # REFACTORING: Extract Method
        game = self._restore_game_from_session(session)

        result = game.dealer_play()
        self._save_game_to_session(session, game)

        # REFACTORING: Extract Method
        return self._process_stay_result(session, result)

    def _process_stay_result(self, session, result):
        """
        Processes the result after a player stays, updating balance based on outcome.
        """
        # REFACTORING: Extract Method
        bet = session.get('bet', 0)

        if "You win" in result:
            self._update_balance(bet * 2)
        elif "tie" in result.lower():
            self._update_balance(bet)

        session['bet'] = 0

        return GameResult(
            session['game'],
            self.get_current_balance(),
            session['bet'],
            result
        ).to_dict()

    def place_bet(self, session, amount):
        """
        Places a bet of the specified amount.
        Uses BetSerializer to validate the bet amount.
        """
        # REFACTORING: Replace Nested Conditional with Guard Clauses
        if 'game' in session and session['game'].get('game_over', False):
            return GameResult(
                session['game'],
                self.get_current_balance(),
                session.get('bet', 0),
                "Game is over. Please start a new game before placing bets."
            ).to_dict()


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

        # REFACTORING: Replace Nested Conditional with Guard Clauses
        if amount == 0:
            self._update_balance(current_bet)
            session['bet'] = 0
        elif self.get_current_balance() >= amount:  # REFACTORING: Replace Temporary Variable with Query
            session['bet'] = current_bet + amount
            self._update_balance(-amount)

        return GameResult(
            session.get('game'),
            self.get_current_balance(),
            session.get('bet', 0),
            "Bet placed successfully."
        ).to_dict()

    def _update_balance(self, amount):
        """
        Updates the user's balance and saves the profile.
        """
        # REFACTORING: Extract Method
        self.profile.balance += amount
        self.profile.save()