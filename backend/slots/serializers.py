from rest_framework import serializers
from .models import Spin, Symbol
from django.contrib.auth import get_user_model

User = get_user_model()

class SymbolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symbol
        fields = ['id', 'name', 'payout_multiplier']
        read_only_fields = ['id', 'name', 'payout_multiplier']

class SpinSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.id')
    user_email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Spin
        fields = ['id', 'user', 'user_id', 'user_email', 'payout', 'result', 'win_data', 'timestamp', 'bet_amount']
        read_only_fields = ['id', 'user', 'payout', 'result', 'win_data', 'timestamp']


class SpinRequestSerializer(serializers.Serializer):
    bet_amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.01, max_value=1000.00)

    def validate_bet_amount(self, value):
        """
        Check if bet amount is within allowed limits and if user has sufficient balance.
        """
        user = self.context['request'].user
        if hasattr(user, 'balance') and user.balance < value:
            raise serializers.ValidationError("Insufficient balance.")

        return value
