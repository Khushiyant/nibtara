import json

import requests
from django.contrib.auth import authenticate
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.token_blacklist.models import (BlacklistedToken,
                                                             OutstandingToken)
from rest_framework_simplejwt.tokens import RefreshToken

from .models import PreTrial, UserAccount
from .serializers import (PreTrialSerializer, UserLoginSerializer,
                          UserRegisterSerializer)

# START: Token Generation


def _get_tokens_for_user(user) -> dict[str, str]:
    """
    Given a user object, returns a dictionary containing the refresh and access tokens for the user.

    Args:
        user: A user object.

    Returns:
        A dictionary containing the refresh and access tokens for the user.
    """
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
# END: Token Generation


class LogoutAPIView(APIView):
    """
    API view to logout a user by blacklisting their refresh token(s).

    If the request data contains "all" key with a truthy value, all refresh tokens for the user will be blacklisted.
    Otherwise, the refresh token provided in the request data will be blacklisted.

    Returns a JSON response with a message and HTTP status code.
    """
    serializer_class = None
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if self.request.data.get("all"):
            token: OutstandingToken
            for token in OutstandingToken.objects.filter(user=request.user):
                _, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response(
                {"message": "OK, goodbye, all refresh tokens blacklisted"}, status=status.HTTP_200_OK)
        refresh_token = self.request.data.get("refresh_token")
        token = RefreshToken(token=refresh_token)
        token.blacklist()
        return Response({"message": "OK, goodbye"}, status=status.HTTP_200_OK)


class LoginAPIView(APIView):
    """
    API view for user login.

    Accepts email and password in the request body and returns JWT tokens if the credentials are valid.
    """
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            data = request.data
            serializer = UserLoginSerializer(data=data)
            if serializer.is_valid():
                email = serializer.validated_data["email"]
                password = serializer.validated_data["password"]

                user = authenticate(email=email, password=password)
                if user:
                    return Response(
                        _get_tokens_for_user(user), status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {"detail": "Invalid credentials"},
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
            return Response(
                {"message": "Something went wrong", "errors": serializer.errors},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except Exception as e:
            return Response(
                {
                    "message": "Something went wrong",
                    "errors": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class RegisterAPIView(APIView):
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            data = request.data

            serializer = UserRegisterSerializer(data=data)
            if serializer.is_valid():
                user = serializer.save()
                tokens = _get_tokens_for_user(user)
                return Response(tokens, status=status.HTTP_201_CREATED)
            return Response(
                {"message": "Something went wrong", "errors": serializer.errors},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        except Exception as e:
            return Response(
                {
                    "message": "Something went wrong",
                    "errors": _(str(e)),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
