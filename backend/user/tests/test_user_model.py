"""
Tests for User model and manager.
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from user.models import Transaction


def create_user(email='testemail@example.com', password='testpassword123'):
    """Helper function to create and return a test user."""
    return get_user_model().objects.create_user(email, password)


class UserModelTests(TestCase):
    """Test User model."""

    def setUp(self):
        """Set up test dependencies."""
        self.email = 'testemail@example.com'
        self.password = 'testpassword123'

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        user = create_user()

        self.assertEqual(user.email, self.email)
        self.assertTrue(user.check_password, self.password)

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email, expected in sample_emails:
            user = create_user(email=email)
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            create_user(email='')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            self.email,
            self.password,
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


class TransactionModelTests(TestCase):
    """Test Transaction model and related functionality."""

    def setUp(self):
        """Set up test dependencies."""
        self.user = create_user()
        self.profile = self.user.profile

    def test_profile_created_with_user(self):
        """Test that a profile is automatically created with a user."""
        self.assertIsNotNone(self.profile)
        self.assertEqual(self.profile.balance, Decimal('0.00'))

    def test_deposit_transaction(self):
        """Test creating a deposit transaction."""
        initial_balance = self.profile.balance
        deposit_amount = 100.00

        new_balance = self.profile.process_transaction(
            amount=deposit_amount,
            transaction_type=Transaction.TransactionType.DEPOSIT
        )

        self.assertEqual(new_balance, initial_balance + deposit_amount)
        self.assertEqual(self.profile.balance, initial_balance + deposit_amount)

        transactions = self.profile.transactions.all()
        self.assertEqual(transactions.count(), 1)

        transaction = transactions.first()
        self.assertEqual(transaction.amount, deposit_amount)
        self.assertEqual(transaction.transaction_type, Transaction.TransactionType.DEPOSIT)
        self.assertEqual(transaction.profile, self.profile)

    def test_withdrawal_transaction(self):
        """Test creating a withdrawal transaction."""
        deposit_amount = 200.00
        self.profile.process_transaction(
            amount=deposit_amount,
            transaction_type=Transaction.TransactionType.DEPOSIT
        )

        initial_balance = self.profile.balance
        withdrawal_amount = 50.00

        new_balance = self.profile.process_transaction(
            amount=withdrawal_amount,
            transaction_type=Transaction.TransactionType.WITHDRAWAL
        )

        self.assertEqual(new_balance, initial_balance - withdrawal_amount)
        self.assertEqual(self.profile.balance, initial_balance - withdrawal_amount)

        transactions = self.profile.transactions.all()
        self.assertEqual(transactions.count(), 2)

        withdrawal = transactions.last()
        self.assertEqual(withdrawal.amount, withdrawal_amount)
        self.assertEqual(withdrawal.transaction_type, Transaction.TransactionType.WITHDRAWAL)

    def test_insufficient_funds_for_withdrawal(self):
        """Test that withdrawal with insufficient funds raises ValidationError."""
        with self.assertRaises(ValidationError):
            self.profile.process_transaction(
                amount=Decimal('100.00'),
                transaction_type=Transaction.TransactionType.WITHDRAWAL
            )

        self.assertEqual(self.profile.transactions.count(), 0)

        self.assertEqual(self.profile.balance, Decimal('0.00'))

    def test_multiple_transactions(self):
        """Test processing multiple transactions."""
        self.profile.process_transaction(
            amount=300.00,
            transaction_type=Transaction.TransactionType.DEPOSIT
        )
        self.profile.process_transaction(
            amount=50.00,
            transaction_type=Transaction.TransactionType.WITHDRAWAL
        )
        self.profile.process_transaction(
            amount=100.00,
            transaction_type=Transaction.TransactionType.DEPOSIT
        )

        expected_balance = 300.00 - 50.00 + 100.00
        self.assertEqual(self.profile.balance, expected_balance)

        transactions = self.profile.transactions.all()
        self.assertEqual(transactions.count(), 3)

        self.assertEqual(transactions[0].transaction_type, Transaction.TransactionType.DEPOSIT)
        self.assertEqual(transactions[1].transaction_type, Transaction.TransactionType.WITHDRAWAL)
        self.assertEqual(transactions[2].transaction_type, Transaction.TransactionType.DEPOSIT)
