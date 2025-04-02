from rest_framework import serializers




class CardSerializer(serializers.Serializer):

    rank = serializers.CharField()
    suit = serializers.CharField()

class GameStateSerializer(serializers.Serializer):

    player_hand = CardSerializer(many=True)
    dealer_hand = CardSerializer(many=True)
    player_score = serializers.IntegerField()
    dealer_score = serializers.IntegerField()
    game_over = serializers.BooleanField()

class BetSerializer(serializers.Serializer):

    amount = serializers.IntegerField(required=True, min_value=0)
