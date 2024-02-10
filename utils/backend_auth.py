from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


class CustomPhoneBackend(ModelBackend):
    def authenticate(self, request, phone=None, email=None, password=None, **kwargs):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(phone=phone, email=email)
        except user_model.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None
