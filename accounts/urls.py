from django.urls import path, re_path

from . import views as auth_views

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(), name="login-view"),
    path("register/", auth_views.RegisterView.as_view(), name="register-view"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout-view"),
    path("valid_email/", auth_views.AjaxRegister.as_view(), name="validate-email"),
    re_path(r"^active/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
            auth_views.ActivateAccount.as_view(), name="active"),
    # password_reset
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
