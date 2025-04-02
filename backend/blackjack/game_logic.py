import random


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank}{self.suit}"

    def to_dict(self):
        return {'rank': self.rank, 'suit': self.suit}


class BlackjackGame:
    def __init__(self):
        self.player_hand = []
        self.dealer_hand = []
        self.deck = []
        self.game_over = False

    def deal_card(self):
        if not self.deck:
            self.create_deck()
        return self.deck.pop()

    def create_deck(self):

        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['♠', '♥', '♣', '♦']
        self.deck = [Card(rank, suit) for suit in suits for rank in ranks]
        random.shuffle(self.deck)
        return self.deck

    def create_deck(self):
        if self.deck:
            return
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['♠', '♥', '♣', '♦']
        self.deck = [Card(rank, suit) for suit in suits for rank in ranks]
        random.shuffle(self.deck)

    def card_value(self, card):
        if card.rank in ['J', 'Q', 'K']:
            return 10
        elif card.rank == 'A':
            return 11
        else:
            return int(card.rank)

    def calculate_hand(self, hand):
        total = sum(self.card_value(card) for card in hand)
        aces = sum(1 for card in hand if card.rank == 'A')


        while total > 21 and aces:
            total -= 10
            aces -= 1

        return total

    def start_game(self):
        self.create_deck()
        self.player_hand = [self.deal_card(), self.deal_card()]
        self.dealer_hand = [self.deal_card(), self.deal_card()]
        self.game_over = False

    def player_hit(self):
        self.player_hand.append(self.deal_card())
        player_score = self.calculate_hand(self.player_hand)

        if player_score > 21:
            self.game_over = True
            return "Bust! You lose."
        elif player_score == 21:
            return "Blackjack! 21 points."
        return None

    def dealer_play(self):

        while self.calculate_hand(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deal_card())

        player_score = self.calculate_hand(self.player_hand)
        dealer_score = self.calculate_hand(self.dealer_hand)

        self.game_over = True


        if dealer_score > 21:
            return "Dealer busts! You win!"
        elif dealer_score == player_score:
            return "It's a tie!"
        elif dealer_score > player_score:
            return "Dealer wins!"
        else:
            return "You win!"

    def get_game_state(self):

        visible_dealer_cards = self.dealer_hand
        if not self.game_over and len(self.dealer_hand) > 0:
            if not self.game_over:
                dealer_hand_repr = [self.dealer_hand[0].to_dict(), {'rank': '?', 'suit': '?'}]
                dealer_score = self.card_value(self.dealer_hand[0])
            else:
                dealer_hand_repr = [card.to_dict() for card in self.dealer_hand]
                dealer_score = self.calculate_hand(self.dealer_hand)

        else:
            dealer_score = self.calculate_hand(self.dealer_hand)

        return {
            'player_hand': [card.to_dict() for card in self.player_hand],
            'dealer_hand': [card.to_dict() for card in self.dealer_hand],
            'player_score': self.calculate_hand(self.player_hand),
            'dealer_score': dealer_score,
            'game_over': self.game_over,
        }