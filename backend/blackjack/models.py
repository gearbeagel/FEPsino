from django.db import models
import random

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank}{self.suit}"

class BlackjackGame(models.Model):
    player_hand = models.JSONField(default=list)
    dealer_hand = models.JSONField(default=list)
    deck = models.JSONField(default=list)
    game_over = models.BooleanField(default=False)

    def create_deck(self):
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['♠', '♥', '♣', '♦']
        deck = [{'rank': rank, 'suit': suit} for suit in suits for rank in ranks]
        random.shuffle(deck)
        return deck

    def deal_card(self):
        return self.deck.pop()

    def card_value(self, card):
        if card['rank'] in ['J', 'Q', 'K']:
            return 10
        elif card['rank'] == 'A':
            return 11
        else:
            return int(card['rank'])

    def calculate_hand(self, hand):
        total = sum(self.card_value(card) for card in hand)
        aces = sum(1 for card in hand if card['rank'] == 'A')
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total

    def start_game(self):
        self.deck = self.create_deck()
        self.player_hand = [self.deal_card(), self.deal_card()]
        self.dealer_hand = [self.deal_card(), self.deal_card()]
        self.game_over = False
        self.save()

    def player_hit(self):
        self.player_hand.append(self.deal_card())
        if self.calculate_hand(self.player_hand) > 21:
            self.game_over = True
            self.save()
            return "Bust! You lose."
        self.save()
        return None

    def dealer_play(self):
        while self.calculate_hand(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deal_card())

        player_score = self.calculate_hand(self.player_hand)
        dealer_score = self.calculate_hand(self.dealer_hand)

        self.game_over = True
        self.save()

        if dealer_score > 21:
            return "Dealer busts! You win!"
        elif dealer_score > player_score:
            return "Dealer wins!"
        elif dealer_score < player_score:
            return "You win!"
        else:
            return "It's a tie!"