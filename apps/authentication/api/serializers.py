from rest_framework import serializers
from drf_yasg.utils import swagger_serializer_method
from apps.authentication.models import (
    CustomUser
)
from apps.authentication.services.users import TokenService


class AuthLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)


class AuthRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)


class TokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)
    access = serializers.CharField(required=True)


class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)


class AuthUserSerializer(serializers.ModelSerializer):
    tokens = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'phone', 'first_name', 'last_name',
            'avatar', 'date_joined', 'tokens'
        ]

    @staticmethod
    @swagger_serializer_method(serializer_or_field=TokenSerializer)
    def get_tokens(obj) -> dict:
        return TokenService().get_token(user=obj)

