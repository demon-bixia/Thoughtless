from django.urls import path

from . import views as auth_views

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(), name="login-view"),
    path("register/", auth_views.RegisterView.as_view(), name="register-view"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout-view"),
]
