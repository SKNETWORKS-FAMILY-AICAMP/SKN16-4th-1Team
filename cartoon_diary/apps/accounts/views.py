"""API views for account operations."""

from __future__ import annotations

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer, SignupSerializer


class SignupView(generics.CreateAPIView):
    """Register a new user account."""

    serializer_class = SignupSerializer
    permission_classes = (permissions.AllowAny,)


class LoginView(APIView):
    """Authenticate a user and return a session placeholder."""

    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        # TODO: integrate JWT/session issuance
        return Response({"detail": "Login successful", "user_id": user.id}, status=status.HTTP_200_OK)
