from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from .serializers import StartDiceGameSerializer
from .game_logic import DiceGame
from .dice import get_figure_factories
from .models import DiceGame as DiceGameModel
from rest_framework_simplejwt.authentication import JWTAuthentication


class DiceGameView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StartDiceGameSerializer
    authentication_classes = [JWTAuthentication]

    @extend_schema(
        request=StartDiceGameSerializer,
        responses={200: dict}
    )
    def post(self, request):
        """ Runs the dice game logic and returns the result."""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            session = request.session
            figure_factories = get_figure_factories()

            user_coins = session.get('user_coins', data['user_coins'])

            bet = data['bet']
            if bet > user_coins:
                return Response({'error': 'Not enough coins!'}, status=status.HTTP_400_BAD_REQUEST)

            user_coins -= bet

            game = DiceGame(session, figure_factories, user_coins)
            result = game.start_game(
                choice1=data['choice1'],
                choice2=data['choice2'],
                bet=bet,
                guessed_number=data['guessed_number']
            )

            new_balance = user_coins + result["payout"]
            session['user_coins'] = new_balance

            DiceGameModel.objects.create(
                user=request.user,
                bet=bet,
                guessed_number=data['guessed_number'],
                choice1=data['choice1'],
                choice2=data['choice2'],
                roll1=result['rolls'][0],
                roll2=result['rolls'][1],
                total=result['total'],
                payout=result['payout'],
                new_balance=new_balance,
            )

            return Response({
                "roll1": result["rolls"][0],
                "roll2": result["rolls"][1],
                "total": result["total"],
                "payout": result["payout"],
                "new_balance": new_balance,
                "message": (
                    "You won!" if result["payout"] > 0
                    else "You lost."
                )
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
