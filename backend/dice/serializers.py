from rest_framework import serializers


class StartDiceGameSerializer(serializers.Serializer):
    choice1 = serializers.ChoiceField(choices=["6", "8", "12"])
    choice2 = serializers.ChoiceField(choices=["6", "8", "12"])
    bet = serializers.IntegerField(min_value=1)
    guessed_number = serializers.IntegerField(min_value=1)
    user_coins = serializers.IntegerField(min_value=0)
