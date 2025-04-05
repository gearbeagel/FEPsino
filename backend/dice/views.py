from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .game_logic import DiceGame
from .dice import get_figure_factories
from .serializers import StartDiceGameSerializer


class DiceGameView(APIView):
    def post(self, request):
        serializer = StartDiceGameSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            facade = DiceGame(request.session, get_figure_factories(), data["user_coins"])
            result = facade.start_game(
                choice1=data["choice1"],
                choice2=data["choice2"],
                bet=data["bet"],
                guessed_number=data["guessed_number"]
            )
            return Response(result)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


