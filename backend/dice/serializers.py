from rest_framework import serializers


class StartDiceGameSerializer(serializers.Serializer):
    choice1 = serializers.ChoiceField(choices=["6", "8", "12"])
    choice2 = serializers.ChoiceField(choices=["6", "8", "12"])
    bet = serializers.IntegerField(min_value=1)
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
