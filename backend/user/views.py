"""
Views for the user API.
"""

import logging

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer

from rest_framework_simplejwt.authentication import JWTAuthentication


logger = logging.getLogger(__name__)


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user
