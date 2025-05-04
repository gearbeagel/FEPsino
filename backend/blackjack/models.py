from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator


User = get_user_model()



class GameHistory(models.Model):
    """
    Model for tracking the history of blackjack games played by users.

    Stores information about each completed game, including:
    - The user who played
    - The amount bet
    - The outcome (win/loss/tie)
    - The final scores
    - The cards in player and dealer hands
    - Timestamps for game start and end
    """

    OUTCOME_WIN = 'win'
    OUTCOME_LOSS = 'loss'
    OUTCOME_TIE = 'tie'
    OUTCOME_CHOICES = [
        (OUTCOME_WIN, 'Win'),
        (OUTCOME_LOSS, 'Loss'),
        (OUTCOME_TIE, 'Tie'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    bet_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    outcome = models.CharField(max_length=10, choices=OUTCOME_CHOICES)
    player_score = models.PositiveSmallIntegerField()
    dealer_score = models.PositiveSmallIntegerField()

    player_hand = models.TextField()
    dealer_hand = models.TextField()

    balance_change = models.IntegerField()

    balance_before = models.PositiveIntegerField()
    balance_after = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'blackjack_gamehistory'
        ordering = ['-created_at']
        verbose_name = 'Game History'
        verbose_name_plural = 'Game Histories'

    def __str__(self):
        """String representation of the game history record."""
        return f"{self.user.username} - {self.outcome} - ${self.bet_amount} on {self.created_at.strftime('%Y-%m-%d %H:%M')}"
