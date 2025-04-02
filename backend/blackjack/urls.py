from django.urls import path, include
from .views import GameStateView, DealCardsView, HitView, StayView, BetView, NewGameView

app_name = 'blackjack_app'


urlpatterns = [



    path('state/', GameStateView.as_view(), name='game-state'),
    path('deal/', DealCardsView.as_view(), name='deal-cards'),
    path('hit/', HitView.as_view(), name='hit'),
    path('stay/', StayView.as_view(), name='stay'),
    path('bet/', BetView.as_view(), name='bet'),
    path('new/', NewGameView.as_view(), name='new-game'),

    ]