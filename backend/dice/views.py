from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import StartDiceGameSerializer
from .services import DiceGameService


class DiceGameView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = StartDiceGameSerializer

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
        user = request.user
        try:
            result = DiceGameService.run_game_logic(user, data)
            return Response(DiceGameService.build_response(result))

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
