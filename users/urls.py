from django.urls import path
from . import views

app_name = "users"
urlpatterns = [
    path("login", views.LoginView.as_view(), name="login"),
    path("login/github", views.github_login, name="github-login"),
    path("login/github/callback", views.github_callback, name="github-callback"),
    path("login/google", views.google_login, name="google-login"),
    path("login/google/callback", views.google_callback, name="google-callback"),
    path("logout", views.log_out, name="logout"),
    path("signup", views.SignupView.as_view(), name="signup"),
    path("verify/<str:key>", views.complete_verification, name="complete-verfication"),
]
