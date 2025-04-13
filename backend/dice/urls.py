from django.urls import path
from .views import DiceGameView

urlpatterns = [
    path("start/", DiceGameView.as_view(), name="dice_game"),
]