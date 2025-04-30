"""
Serializers for the user API View.
"""

from django.contrib.auth import get_user_model
from rest_framework import serializers

from user.models import Profile, Transaction


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for the user profile object."""
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['user', 'username', 'balance']
        read_only_fields = ['balance']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        password = user_data.pop('password', None)

        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        if password:
            user.set_password(password)
        user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for transaction history."""

    class Meta:
        model = Transaction
        fields = ['amount', 'transaction_type', 'date']
        read_only_fields = ['date']
