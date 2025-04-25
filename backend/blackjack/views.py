from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .facade import BlackjackGameFacade
from .serializers import BetSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication


authentication_classes = [JWTAuthentication]
"""Views for the Blackjack game app."""

class GameStateView(APIView):
    """View to get the current game state"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get current game state"""
        facade = BlackjackGameFacade(request.user)
        result = facade.get_game_state(request.session)
        return Response(result)


class DealCardsView(APIView):
    """View to deal initial cards"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Deal initial cards to start the game"""
        facade = BlackjackGameFacade(request.user)
        result = facade.deal_cards(request.session)
        return Response(result)


class HitView(APIView):
    """View to hit (take another card)"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Player takes another card"""
        facade = BlackjackGameFacade(request.user)
        result = facade.player_hit(request.session)
        return Response(result)


class StayView(APIView):
    """View to stay (end turn)"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Player stands with current cards"""
        facade = BlackjackGameFacade(request.user)
        result = facade.player_stay(request.session)
        return Response(result)


class BetView(APIView):
    """View to place a bet"""
    serializer_class = BetSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Place a bet"""
        serializer = BetSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            facade = BlackjackGameFacade(request.user)
            result = facade.place_bet(request.session, amount)
            return Response(result)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NewGameView(APIView):
    """View to start a new game"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Start a new game"""
        facade = BlackjackGameFacade(request.user)
        result = facade.start_new_game(request.session)
        return Response(result)
