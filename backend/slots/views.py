from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Spin, Symbol
from .serializers import (
    UserSerializer, SpinSerializer,
    SymbolSerializer, SpinRequestSerializer, RegistrationSerializer
)
from .services import SlotMachineService


class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        description="Register a new user",
        responses={201: UserSerializer}
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Return the user data for the newly created user
        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED
        )


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    @extend_schema(
        description="Get current user information",
        responses={200: UserSerializer}
    )
    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class SpinViewSet(viewsets.GenericViewSet):
    serializer_class = SpinSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Spin.objects.filter(user=self.request.user)

    @extend_schema(
        description="Spin the slot machine",
        request=SpinRequestSerializer,
        responses={200: dict}  # Using dict as we return custom format
    )
    @action(detail=False, methods=['post'])
    def spin(self, request):
        serializer = SpinRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        bet_size = serializer.validated_data['bet_size']

        # Get the current user
        user = request.user

        # Create the spin
        slot_machine = SlotMachineService()
        result = slot_machine.play_spin(user, bet_size)

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