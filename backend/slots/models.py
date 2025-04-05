from django.db import models
from django.contrib.auth.models import User
import uuid


class Symbol(models.Model):
    name = models.CharField(max_length=50)
    image_path = models.CharField(max_length=200)
    payout_multiplier = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)

    def __str__(self):
        return self.name

    @classmethod
    def create_default_symbols(cls):
        """Create default symbols that match the frontend."""
        symbols = [
            {'name': 'star', 'image_path': 'star.svg', 'multiplier': 3.0},
            {'name': 'heart', 'image_path': 'heart.svg', 'multiplier': 2.5},
            {'name': 'cherry', 'image_path': 'cherry.svg', 'multiplier': 2.0},
            {'name': 'gem', 'image_path': 'gem.svg', 'multiplier': 1.5},
            {'name': 'citrus', 'image_path': 'citrus.svg', 'multiplier': 1.0},
        ]

        for symbol_data in symbols:
            cls.objects.get_or_create(
                name=symbol_data['name'],
                defaults={
                    'image_path': symbol_data['image_path'],
                    'payout_multiplier': symbol_data['multiplier']
                }
            )


class Spin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='spins')
    bet_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payout = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    result = models.JSONField()  # Store the spin result as JSON
    win_data = models.JSONField(null=True, blank=True)  # Win information
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Spin {self.id} for User {self.user.username}"