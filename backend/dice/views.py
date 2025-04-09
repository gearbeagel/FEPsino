from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from .serializers import StartDiceGameSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from .services import DiceGameService


class DiceGameView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StartDiceGameSerializer
    authentication_classes = [JWTAuthentication]

    @extend_schema(
        request=StartDiceGameSerializer,
        responses={200: dict}
    )
    def post(self, request):
        """Runs the dice game logic and returns the result."""
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        session = request.session

        user_coins = DiceGameService.get_user_coins(session, data)
        bet = data['bet']
        if bet > user_coins:
            return Response({'error': 'Not enough coins!'}, status=status.HTTP_400_BAD_REQUEST)

        result = DiceGameService.run_game_logic(session, user_coins, data)
        DiceGameService.save_game_to_db(request.user, data, result)

        return Response(DiceGameService.build_response(result))
