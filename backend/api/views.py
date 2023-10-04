import json

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

from .filters import LawyerFilter, PreTrialFilter
from .models import Judge, Lawyer, PreTrial, UserAccount
from .serializers import (JudgeRegisterationSerializer,
                          LawyerRegisterationSerializer, PreTrialSerializer,
                          UserLoginSerializer, UserRegistrationSerializer)

# START: Token Generation


def _get_tokens_for_user(user) -> dict[str, str]:
    """
    Given a user object, returns a dictionary containing the refresh and access tokens for the user.

    Args:
    -----
        user: A user object.

    Returns:
    -------
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


class UserRegisterAPIView(APIView):
    """
    API view for user registration.

    Methods:
    --------
    post(request):
        Registers a new user and returns authentication tokens.

    Attributes:
    -----------
    serializer_class: UserRegistrationSerializer
        Serializer class for user registration.
    permission_classes: tuple
        Tuple of permission classes for the view.
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Registers a new user and returns authentication tokens.

        Parameters:
        -----------
        request: Request
            HTTP request object.

        Returns:
        --------
        Response:
            HTTP response object containing authentication tokens.
        """
        try:
            data = request.data

            serializer = self.serializer_class(data=data)
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


class LawyerRegisterAPIView(APIView):
    """
    API view to register a lawyer.

    Methods:
    --------
    post(self, request):
        Registers a lawyer with the provided details in the request data.

    Attributes:
    -----------
    serializer_class: Serializer class
        Serializer class to serialize and deserialize the request and response data.
    permission_classes: tuple
        Tuple of permission classes that the user must have to access this view.
    """

    serializer_class = LawyerRegisterationSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            context = request.data.copy()
            user = UserAccount.objects.get(pk=request.user.id)
            user.user_type = UserAccount.Roles.LAWYER
            user.save()
            context['user'] = user.id

            serializer = self.serializer_class(data=context)
            if serializer.is_valid():
                lawyer = serializer.save()
                return Response(
                    {"message": "Lawyer registered successfully", "lawyer": lawyer},
                    status=status.HTTP_201_CREATED,
                )
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


class JudgeRegisterAPIView(APIView):
    """
    API view for registering a Judge.

    Methods:
    --------
    post(self, request):
        Registers a Judge with the provided details in the request data.

    Attributes:
    -----------
    serializer_class : JudgeRegisterationSerializer
        Serializer class for validating and deserializing the request data.
    permission_classes : tuple
        Tuple of permission classes that the user must have to access this view.
    """

    serializer_class = JudgeRegisterationSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            context = request.data.copy()
            user = UserAccount.objects.get(pk=request.user.id)
            user.user_type = UserAccount.Roles.JUDGE
            user.save()
            context['user'] = user.id

            serializer = self.serializer_class(data=context)
            if serializer.is_valid():
                lawyer = serializer.save()
                return Response(
                    {"message": "Lawyer registered successfully", "lawyer": lawyer},
                    status=status.HTTP_201_CREATED,
                )
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


# TODO: base user data
class ListLawyersAPIView(APIView):
    """
    API view to list lawyers based on lawyer_type and paginate the results.
    """
    serializer_class = None
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        context: dict = {}
        filtered_users = None
        try:

            lawyer_type = request.GET.get('lawyer_type', Lawyer.Roles.CIVIL)
            filtered_users = LawyerFilter(
                request.GET, queryset=Lawyer.objects.filter(lawyer_type=lawyer_type).order_by('-id'))

            context['filtered_users'] = json.loads(
                serialize("json", filtered_users.qs))

            # Pagination
            print(filtered_users.qs)
            paginated_users = Paginator(filtered_users.qs, 10)
            page_number = request.GET.get('page')
            page_obj = paginated_users.get_page(
                page_number) if page_number else paginated_users.get_page(1)

            context['page_obj'] = json.loads(serialize("json", page_obj))

            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {
                    "message": "Something went wrong",
                    "errors": _(str(e)),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class ListPreTrialsAPIView(APIView):
    """
    API endpoint that returns a list of pre-trials for the authenticated user.
    """
    serializer_class = None
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        GET request handler for the ListPreTrialsAPIView.
        """
        context: dict = {}
        user = request.user
        filtered_pretrials = None
        try:
            filtered_pretrials = PreTrialFilter(
                request.GET, queryset=PreTrial.objects.all().filter(user__email=user.email).order_by('date_registered'))

            context['filtered_pretrials'] = json.loads(
                serialize("json", filtered_pretrials.qs))

            # Pagination
            print(filtered_pretrials.qs)
            paginated_pretrials = Paginator(filtered_pretrials.qs, 10)
            page_number = request.GET.get('page')
            page_obj = paginated_pretrials.get_page(
                page_number) if page_number else paginated_pretrials.get_page(1)

            context['page_obj'] = json.loads(serialize("json", page_obj))

            return Response(context, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {
                    "message": "Something went wrong",
                    "errors": _(str(e)),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
