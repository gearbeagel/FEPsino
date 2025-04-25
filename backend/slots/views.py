from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Spin, Symbol
from .serializers import SpinSerializer,SymbolSerializer, SpinRequestSerializer
from .services import SlotMachineService




class SpinViewSet(viewsets.GenericViewSet):
    serializer_class = SpinSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return Spin.objects.filter(user=self.request.user)

    @extend_schema(
        description="Spin the slot machine",
        request=SpinRequestSerializer,
        responses={200: dict}  # Using dict as we return custom format
    )
    @action(detail=False, methods=['post'])
    def spin(self, request):
        serializer = SpinRequestSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        bet_amount = serializer.validated_data['bet_amount']

        # Get the current user
        user = request.user

        # Create the spin
        slot_machine = SlotMachineService()
        result = slot_machine.play_spin(user, bet_amount)

        # Return the spin result in format compatible with frontend
        return Response(result)

    @extend_schema(
        description="Get user's spin history",
        responses={200: SpinSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def history(self, request):
        spins = Spin.objects.filter(user=request.user).order_by('-timestamp')

        # Optional pagination could be added here
        serializer = self.get_serializer(spins, many=True)
        return Response(serializer.data)


class SymbolViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Symbol.objects.all()
    serializer_class = SymbolSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @extend_schema(
        description="Get symbols with frontend mapping",
        responses={200: dict}
    )
    @action(detail=False, methods=['get'])
    def frontend_mapping(self, request):
        """Return mapping between backend symbols and frontend indexes"""
        from .services import ReelService
        reel_service = ReelService(Symbol.objects.all())

        return Response({
            'backend_to_frontend': reel_service.backend_symbol_map,
            'frontend_to_backend': reel_service.frontend_symbol_map
        })
