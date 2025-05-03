from django.urls import path
from .views import GameStateView, HitView, StayView, BetView
"""Urls for the Blackjack game app."""



app_name = 'blackjack_app'


urlpatterns = [
    path('state/', GameStateView.as_view(), name='game-state'),
    # GET: Returns the current state of the game, including hands, scores, and game status.

    path('hit/', HitView.as_view(), name='hit'),
    # POST: Player requests an additional card. Checks for bust.

    path('stay/', StayView.as_view(), name='stay'),
    # POST: Player ends their turn. Dealer plays and final results are returned.

    path('bet/', BetView.as_view(), name='bet'),
    # POST: Places a bet, starts a new game and deals cards. Requires "amount" field in JSON body.
]