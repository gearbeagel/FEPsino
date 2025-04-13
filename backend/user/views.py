"""
Views for the user API.
"""
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user.serializers import UserSerializer, TransactionSerializer, ProfileSerializer

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = ProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user.profile


class LogoutView(APIView):
    """Logout the user by blacklisting the refresh token."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            response_msg = {"message": "Logout successful."}
            return Response(response_msg, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            error = {"error": "Invalid token or token already blacklisted."}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)


class TransactionView(generics.CreateAPIView):
    """
    Process a deposit or withdrawal.
    Expecting fields:
      - amount: Decimal
      - transaction_type: One of ('DEPOSIT', 'WITHDRAWAL')
    """
    serializer_class = TransactionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        amount = serializer.validated_data['amount']
        transaction_type = serializer.validated_data['transaction_type']

        new_balance = user.profile.process_transaction(amount, transaction_type)
        self.new_balance = new_balance

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            response_data = {
                'status': f'Balance updated successfully.',
                'new_balance': self.new_balance,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
