from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .facade import BlackjackGameFacade
from .serializers import BetSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

"""Views for the Blackjack game app."""


class GameStateView(APIView):
    """View to get the current game state"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        """Get current game state"""
        facade = BlackjackGameFacade(request.user)
        result = facade.get_game_state(request.session)
        return Response(result)


class HitView(APIView):
    """View to hit (take another card)"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        """Player takes another card"""
        facade = BlackjackGameFacade(request.user)
        result = facade.player_hit(request.session)
        return Response(result)


class StayView(APIView):
    """View to stay (end turn)"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        """Player stands with current cards"""
        facade = BlackjackGameFacade(request.user)
        result = facade.player_stay(request.session)
        return Response(result)


class BetView(APIView):
    """View to place a bet, start a new game and deal cards"""
    serializer_class = BetSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = BetSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            facade = BlackjackGameFacade(request.user)
            result = facade.start_new_game_with_bet(request.session, amount)

            # If there's an error message, only return the message
            if 'message' in result and ('Insufficient balance' in result['message'] or
                                        'Invalid bet amount' in result['message'] or
                                        'Cannot change bet' in result['message']):
                return Response({'message': result['message']}, status=status.HTTP_400_BAD_REQUEST)

            # Success case: return simple confirmation
            return Response({'message': 'Bet placed and game started'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)