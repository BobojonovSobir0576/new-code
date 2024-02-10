from django.utils import timezone
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from apps.authentication.managers.custom_manager import CustomUserManager
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class AuthType(models.TextChoices):
        LOGIN_PASSWORD_AUTH = "login_password_auth", _("Email and Password Authentication")

    class Text:
        WRONG_PASSWORD_OR_LOGIN_ENTERED = 'Wrong login or password'
        USER_WITH_SUCH_EMAIL_ALREADY_EXISTS = 'A user with this email already exists'
        USER_WITH_SUCH_EMAIL_DOES_NOT_EXIST = "User with this email does not exist"
        RESET_PASSWORD_SUBJECT = "Password recovery request"
        RESET_PASSWORD_MESSAGE = (
            "You or someone else has requested to restore access to your account {user_email}<br>"
            "Your password recovery link \n{link}"
        )
        RESET_LINK_SUCCESS = "A letter with a link has been sent by email"
        RESET_PASSWORD_SUCCESS = "Your password has been successfully updated."
        TOKEN_USED = "Token has already been used."
        TOKEN_NOT_EXIST = "The token does not exist."
        USER_DELETED = "The user has already been deleted."

    email = models.EmailField(_('Email'), unique=True, null=True, blank=False)
    phone = models.CharField(_('Phone'), max_length=30, blank=False, null=True)
    first_name = models.CharField(_('First name'), max_length=255, null=True, blank=True)
    last_name = models.CharField(_('Lsat name'), max_length=255, null=True, blank=True)
    avatar = models.ImageField(_('Avatar'), upload_to="avatar/", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone"]

    def __str__(self):
        return self.phone

    class Meta:
        db_table = "table_user"
        verbose_name = "CustomUser"
        verbose_name_plural = "CustomUsers"
