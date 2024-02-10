from django.db import transaction
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.tokens import RefreshToken
from utils.main import object_get_or_none
from apps.authentication.models import CustomUser
from django.conf import settings


class TokenService:
    @staticmethod
    def get_token(user: CustomUser) -> dict:
        """Receiving a token"""

        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def refresh_token(self, token_refresh) -> dict:
        """Token update"""

        valid_data = TokenBackend(
            algorithm=settings.SIMPLE_JWT["ALGORITHM"], signing_key=settings.SIMPLE_JWT["SIGNING_KEY"]
        ).decode(token_refresh, verify=True)

        user_id = valid_data.get("user_id")
        user = CustomUser.objects.get(id=user_id)
        return self.get_token(user)


class UserService:
    @staticmethod
    def create_user(**kwargs) -> CustomUser:
        user = CustomUser.objects.create_user(**kwargs)
        return user

    @staticmethod
    def user_exists(email) -> bool:
        """Checking user existence by email"""

        return CustomUser.objects.filter(email=email).exists()

    @staticmethod
    def get_user(email) -> CustomUser:
        """Receiving a user by email"""

        return CustomUser.objects.get(email=email)

    @staticmethod
    def get_user_by_id(user_id) -> CustomUser:
        """Getting user by id"""

        return CustomUser.objects.get(id=user_id)


class AuthService:
    @staticmethod
    @transaction.atomic
    def register_user(**kwargs) -> CustomUser:
        """User registration"""
        user_service = UserService()
        if user_service.user_exists(kwargs.get("email")):
            raise ValueError(CustomUser.Text.USER_WITH_SUCH_EMAIL_ALREADY_EXISTS)
        user = user_service.create_user(**kwargs)
        return user

    @staticmethod
    def authenticate_user(email, password) -> CustomUser:
        """User authentication"""
        user = object_get_or_none(CustomUser, email=email)
        if user and user.check_password(password):
            return user
        raise ValueError(CustomUser.Text.WRONG_PASSWORD_OR_LOGIN_ENTERED)

