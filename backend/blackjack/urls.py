from django.urls import path
from .views import GameStateView, DealCardsView, HitView, StayView, BetView, NewGameView

"""Urls for the Blackjack game app."""



app_name = 'blackjack_app'


urlpatterns = [
    path('state/', GameStateView.as_view(), name='game-state'),
    # GET: Returns the current state of the game, including hands, scores, and game status.

    path('deal/', DealCardsView.as_view(), name='deal-cards'),
    # POST: Deals two cards to both the player and dealer to start the game.

    path('hit/', HitView.as_view(), name='hit'),
    # POST: Player requests an additional card. Checks for bust.

    path('stay/', StayView.as_view(), name='stay'),
    # POST: Player ends their turn. Dealer plays and final results are returned.

    path('bet/', BetView.as_view(), name='bet'),
    # POST: Places a bet before the game starts. Requires "amount" field in JSON body.

    path('new/', NewGameView.as_view(), name='new-game'),
    # POST: Resets and initializes a new game session.
]
