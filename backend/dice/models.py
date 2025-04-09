from django.db import models
from user.models import User


class DiceGameModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bet = models.IntegerField()
    guessed_number = models.IntegerField()
    choice1 = models.CharField(max_length=2)
    choice2 = models.CharField(max_length=2)
    roll1 = models.IntegerField()
    roll2 = models.IntegerField()
    total = models.IntegerField()
    payout = models.IntegerField()
    new_balance = models.IntegerField()

    def __str__(self):
        return f"{self.user.user_name}'s game with bet {self.bet}"

    def save_game_result(self):
        self.save()
