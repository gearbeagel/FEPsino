from decimal import Decimal
from rest_framework import serializers


class StartDiceGameSerializer(serializers.Serializer):
    VALID_DICE_CHOICES = [6, 8, 12]

    choice1 = serializers.ChoiceField(choices=VALID_DICE_CHOICES)
    choice2 = serializers.ChoiceField(choices=VALID_DICE_CHOICES)
    bet = serializers.DecimalField(min_value=Decimal('0.01'), max_digits=10, decimal_places=2)
    guessed_number = serializers.IntegerField(min_value=2)

    def validate(self, data):
        """Validates that the guessed number is within the valid range based on the selected dice."""
        choice1_faces = int(data['choice1'])
        choice2_faces = int(data['choice2'])
        max_possible_sum = choice1_faces + choice2_faces
        min_possible_sum = 2

        if not (min_possible_sum <= data['guessed_number'] <= max_possible_sum):
            raise serializers.ValidationError({
                'guessed_number': f"Value must be between {min_possible_sum} and {max_possible_sum} based on selected dice."
            })

        return data
