from utils.generic.generic_api_view import GenericAPIView
from apps.authentication.api import serializers as auth_serializers
from apps.authentication.models import CustomUser
from apps.authentication.services import users as user_services
from rest_framework import permissions, status
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema




class AuthModelViewSet(GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = auth_serializers.AuthLoginSerializer
    permission_classes = (permissions.AllowAny,)
    SERIALIZER = {
        "register": {
            "request": auth_serializers.AuthRegisterSerializer,
            "response": auth_serializers.AuthUserSerializer,
        },
        "login": {
            "request": auth_serializers.AuthLoginSerializer,
            "response": auth_serializers.AuthUserSerializer,
        },
        "refresh_token": {
            "request": auth_serializers.TokenRefreshSerializer,
            "response": auth_serializers.TokenSerializer,
        }
    }

    auth_service = user_services.AuthService()
    # email_service = user_services.EmailService()
    user_service = user_services.UserService()
    token_service = user_services.TokenService()

    @swagger_auto_schema(
        request_body=SERIALIZER["register"]["request"],
        responses={
            201: SERIALIZER["register"]["response"],
            404: openapi.Response(
                description="Example response if email already exists",
                examples={"application/json": {"detail": CustomUser.Text.USER_WITH_SUCH_EMAIL_ALREADY_EXISTS}},
            ),
        },
    )
    def register(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = self.auth_service.register_user(**serializer.data)
            data = self.get_serializer_response(user)
            return Response(data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=SERIALIZER["login"]["request"],
        responses={
            201: SERIALIZER["login"]["response"],
            404: openapi.Response(
                description="An example of a response in case of an incorrect login or password",
                examples={"application/json": {"detail": CustomUser.Text.WRONG_PASSWORD_OR_LOGIN_ENTERED}},
            ),
        },
    )
    def login(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data.get("email")
        password = serializer.data.get("password")

        try:
            user = self.auth_service.authenticate_user(email, password)
            data = self.get_serializer_response(user)
            return Response(data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        request_body=SERIALIZER["refresh_token"]["request"],
        responses={
            201: SERIALIZER["refresh_token"]["response"],
            400: openapi.Response(
                description="An example of a response when the token is invalid or has expired.",
                examples={"application/json": {"detail": "Token is invalid or expired"}},
            ),
            401: openapi.Response(
                description="Example response for an invalid token",
                examples={
                    "application/json": {
                        "detail": "This token is not valid for any token type",
                        "code": "token_not_valid",
                        "messages": [
                            {
                                "token_class": "AccessToken",
                                "token_type": "access",
                                "message": "Token is invalid or expired",
                            }
                        ],
                    }
                },
            ),
        },
    )
    def refresh_token(self, request, *args, **kwargs):
        """
        If, when using a token, an error is returned with status = 401 and code = token_not_valid,
         you need to use this endpoint (the request updates the access and refresh tokens).
         If, when using a refresh token, error 40x is returned, you need to re-login (auth/login/)
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token_refresh = serializer.data.get("refresh")
        try:
            token = self.token_service.refresh_token(token_refresh=token_refresh)
            data = self.get_serializer_response(token)
            return Response(data)
        except Exception as error:
            return Response({"detail": str(error)}, status=status.HTTP_400_BAD_REQUEST, exception=True)
