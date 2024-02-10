from django.urls import path
from apps.authentication.api.views import auth_views

app_name = "auth"
urlpatterns = [
    path("login/", auth_views.AuthModelViewSet.as_view({"post": "login"}), name="login"),
    path("register/", auth_views.AuthModelViewSet.as_view({"post": "register"}), name="register"),
    path("token/refresh/", auth_views.AuthModelViewSet.as_view({"post": "refresh_token"}), name="token_refresh"),
]