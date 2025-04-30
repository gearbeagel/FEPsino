"""
Database model for User API.
"""
import logging

from django.contrib.auth.base_user import (AbstractBaseUser, BaseUserManager)
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from core import settings
from user.utils import generate_random_username


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user"""
        if not email:
            raise ValueError('User must have an email')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create, save and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""

    email = models.EmailField(max_length=255, unique=True)
    coin_balance = models.IntegerField(default=1000) #I use coins from here temporarily
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class Transaction(models.Model):
    """Transaction history for a user"""

    class TransactionType(models.TextChoices):
        DEPOSIT = 'DEPOSIT', 'Deposit'
        WITHDRAWAL = 'WITHDRAWAL', 'Withdrawal'

    profile = models.ForeignKey(
        'Profile',
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    date = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(
        max_length=20,
        choices=TransactionType.choices
    )

    def __str__(self):
        return f"{self.profile.user.email} - {self.transaction_type} of {self.amount} on {self.date}"


class Profile(models.Model):
    """User's profile"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    username = models.CharField(max_length=50, default=generate_random_username)
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )

    def __str__(self):
        return f"{self.user.email}'s profile"

    def add_balance(self, amount):
        """Add some amount to user's balance."""
        self.balance += amount
        self.save()

    def deduct_balance(self, amount):
        """Deduct some amount from user's balance."""
        self.balance -= amount
        self.save()

    def process_transaction(self, amount, transaction_type):
        """
        Update balance and record a transaction.
        Raises a ValidationError if a withdrawal would lead to a negative balance.
        """
        if transaction_type == Transaction.TransactionType.WITHDRAWAL:
            if self.balance < amount:
                from rest_framework.exceptions import ValidationError
                raise ValidationError("Insufficient funds for withdrawal.")

            self.deduct_balance(amount)
        elif transaction_type == Transaction.TransactionType.DEPOSIT:
            self.add_balance(amount)

        self.transactions.create(
            amount=amount,
            transaction_type=transaction_type
        )
        return self.balance
