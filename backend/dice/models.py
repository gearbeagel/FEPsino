from decimal import Decimal
from django.db import models
from user.models import User


class DiceGameModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bet = models.DecimalField(max_digits=10, decimal_places=2)
    guessed_number = models.IntegerField()
    choice1 = models.CharField(max_length=2)
    choice2 = models.CharField(max_length=2)
    roll1 = models.IntegerField()
    roll2 = models.IntegerField()
    total = models.IntegerField()
    payout = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.email}'s game with bet {self.bet}"
