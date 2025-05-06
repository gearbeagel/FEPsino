from rest_framework import serializers
from .models import GameHistory

"""
Serializers for the Blackjack game logic.
Contains serializers for card, game state, and bets.
"""





class CardSerializer(serializers.Serializer):
    """
    Serializer representing a single playing card.

    Fields:
        rank (CharField): The rank of the card (e.g., '2', '10', 'J', 'Q', 'K', 'A').
        suit (CharField): The suit of the card (e.g., '♠', '♥', '♣', '♦').

    Example:
        {
            "rank": "A",
            "suit": "♠"
        }
    """
    rank = serializers.CharField()
    suit = serializers.CharField()

class GameStateSerializer(serializers.Serializer):
    """
    Serializer representing the state of a Blackjack game.

    Fields:
        player_hand (List[CardSerializer]): The current cards in the player's hand.
        dealer_hand (List[CardSerializer]): The current cards in the dealer's hand.
        player_score (IntegerField): The total value of the player's hand.
        dealer_score (IntegerField): The total value of the dealer's hand.
        game_over (BooleanField): Indicates whether the game has ended.

    Example:
        {
            "player_hand": [{"rank": "A", "suit": "♠"}, {"rank": "10", "suit": "♦"}],
            "dealer_hand": [{"rank": "9", "suit": "♥"}, {"rank": "7", "suit": "♣"}],
            "player_score": 21,
            "dealer_score": 16,
            "game_over": false
        }
    """
    player_hand = CardSerializer(many=True)
    dealer_hand = CardSerializer(many=True)
    player_score = serializers.IntegerField()
    dealer_score = serializers.IntegerField()
    game_over = serializers.BooleanField()


class BetSerializer(serializers.Serializer):
    """
    Serializer for placing a bet in the Blackjack game.

    Fields:
        amount (IntegerField): The bet amount placed by the player.
            Must be a non-negative integer (min_value=0).

    Example:
        {
            "amount": 100
        }
    """
    amount = serializers.IntegerField(required=True, min_value=0)


