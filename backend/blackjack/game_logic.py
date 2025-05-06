import random


class Card:
    """
    Represents a playing card with a rank and suit.
    """

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank}{self.suit}"

    def to_dict(self):
        """
        Converts card to dictionary representation for serialization.
        """
        return {'rank': self.rank, 'suit': self.suit}


class BlackjackGame:
    """
    Implements the rules and logic for a blackjack card game.
    """

    # REFACTORING: Extract Constants
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    SUITS = ['♠', '♥', '♣', '♦']

    def __init__(self):
        self.player_hand = []
        self.dealer_hand = []
        self.deck = []
        self.game_over = False

    def deal_card(self):
        """
        Deals a card from the deck, creating a new deck if necessary.
        """
        if not self.deck:
            self.create_deck()
        return self.deck.pop()

    def create_deck(self):
        """
        Creates and shuffles a standard 52-card deck if one doesn't exist.
        """
        if self.deck:
            return  # Якщо колода вже існує, не створюємо нову

        self.deck = [Card(rank, suit) for suit in self.SUITS for rank in self.RANKS]
        random.shuffle(self.deck)

    def card_value(self, card):
        """
        Returns the numerical value of a card for blackjack scoring.
        """
        # REFACTORING: Replace Nested Conditional with Guard Clauses
        if card.rank in ['J', 'Q', 'K']:
            return 10
        if card.rank == 'A':
            return 11
        return int(card.rank)

    # REFACTORING: Replace Temporary Variable with Query
    def get_hand_score(self, hand):
        """
        Returns the current score of a hand.
        """
        return self.calculate_hand(hand)

    def calculate_hand(self, hand):
        """
        Calculates the total value of a hand, accounting for ace values.
        """
        total = sum(self.card_value(card) for card in hand)
        # REFACTORING: Simplify calculation of aces count
        aces = len([card for card in hand if card.rank == 'A'])


        while total > 21 and aces:
            total -= 10
            aces -= 1

        return total

    def start_game(self):
        """
        Initializes a new game with fresh deck and hands.
        """
        self.create_deck()
        # REFACTORING: Extract Method - deal initial cards
        self._deal_initial_cards()
        self.game_over = False

    def _deal_initial_cards(self):
        """
        Deals the initial cards to player and dealer.
        """
        self.player_hand = [self.deal_card(), self.deal_card()]
        self.dealer_hand = [self.deal_card(), self.deal_card()]

    def player_hit(self):
        """
        Processes a player's request for another card and returns the result.
        """
        self.player_hand.append(self.deal_card())
        # REFACTORING: Replace Temporary Variable with Query
        player_score = self.get_hand_score(self.player_hand)

        # REFACTORING: Replace Nested Conditional with Guard Clauses
        if player_score > 21:
            self.game_over = True
            return "Bust! You lose."
        if player_score == 21:
            return "Blackjack! 21 points."
        return None

    def dealer_play(self):
        """
        Executes dealer's play according to standard rules and determines the winner.
        """
        # REFACTORING: Extract Method - dealer draws cards
        self._dealer_draw_cards()

        # REFACTORING: Replace Temporary Variable with Query
        player_score = self.get_hand_score(self.player_hand)
        dealer_score = self.get_hand_score(self.dealer_hand)

        self.game_over = True

        # REFACTORING: Extract Method - determine game outcome
        return self._determine_outcome(player_score, dealer_score)

    def _dealer_draw_cards(self):
        """
        Dealer draws cards until reaching at least 17 points.
        """
        # REFACTORING: Replace Temporary Variable with Query
        while self.get_hand_score(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deal_card())

    def _determine_outcome(self, player_score, dealer_score):
        """
        Determines the game outcome based on final scores.
        """
        # REFACTORING: Replace Nested Conditional with Guard Clauses
        if dealer_score > 21:
            return "Dealer busts! You win!"
        if dealer_score == player_score:
            return "It's a tie!"
        if dealer_score > player_score:
            return "Dealer wins!"
        return "You win!"

    def get_game_state(self):
        """
        Returns the current game state as a dictionary.
        """
        player_score = self.get_hand_score(self.player_hand)

        if self.game_over or not self.dealer_hand:
            dealer_score = self.get_hand_score(self.dealer_hand)
            dealer_hand_repr = [card.to_dict() for card in self.dealer_hand]
        else:

            dealer_score = self.card_value(self.dealer_hand[0]) if self.dealer_hand else 0
            if self.dealer_hand:
                dealer_hand_repr = [self.dealer_hand[0].to_dict()]

            else:
                dealer_hand_repr = []

        game_state = {
            'player_hand': [card.to_dict() for card in self.player_hand],
            'dealer_hand': dealer_hand_repr,
            'player_score': player_score,
            'dealer_score': dealer_score,
            'game_over': self.game_over,

        }

        return game_state
