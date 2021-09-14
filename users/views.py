import requests
from django.views.generic import FormView
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile
from . import forms, models, oauth_providers


class LoginView(FormView):
    """Login View"""

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class SignupView(FormView):
    """Signup View"""

    template_name = "users/signup.html"
    form_class = forms.SignupForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
            user.verify_email()
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
    except models.User.DoesNotExist:
        pass
    return redirect(reverse("core:home"))


def github_login(request):
    social_client = "github"
    scope = "read:user user:email"
    auth_provider = oauth_providers.OauthProvider(
        request=request, social_client=social_client, scope=scope
    )
    try:
        return redirect(auth_provider.request_auth())
    except Exception:
        return redirect(reverse("users:login"))


def github_callback(request):
    try:
        social_client = "github"
        auth_provider = oauth_providers.OauthProvider(
            request=request, social_client=social_client
        )
        token = auth_provider.get_access_token()
        git_user = auth_provider.get_user(token)
        if git_user.get("login"):
            user_name = git_user.get("name").split()
            first_name = user_name[0]
            last_name = user_name[-1] if len(user_name) > 1 else None

            user_info = {
                "email": git_user.get("email"),
                "username": git_user.get("email"),
                "first_name": first_name,
                "last_name": last_name,
                "bio": git_user.get("bio"),
                "avatar_url": git_user.get("avatar_url"),
            }

            if user_info["email"] is None:
                git_user_emails = auth_provider.get_user(token, "/emails")
                email = next(
                    (
                        git_user_email["email"]
                        for git_user_email in git_user_emails
                        if git_user_email["primary"] is True
                    ),
                    git_user_emails[0]["email"],
                )

                if email is None:
                    raise oauth_providers.OauthException()
                else:
                    user_info["email"] = email
                    user_info["username"] = email

            return user_access(request, user_info, models.User.LOGIN_GITHUB)
        else:
            raise oauth_providers.OauthException()
    except Exception as e:
        # print("%s (%s)" % (e.message, type(e)))
        return redirect(reverse("users:login"))


def google_login(request):
    social_client = "google"
    scope = "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile"
    extra_params = {
        "response_type": "code",
        "approval_prompt": "force",
        "access_type": "offline",
    }

    auth_provider = oauth_providers.OauthProvider(
        request=request, social_client=social_client, scope=scope
    )
    auth_provider.extra_params = extra_params
    try:
        return redirect(auth_provider.request_auth())
    except Exception:
        return redirect(reverse("users:login"))


def google_callback(request):
    try:
        social_client = "google"
        auth_provider = oauth_providers.OauthProvider(
            request=request, social_client=social_client
        )

        token = auth_provider.get_access_token()
        google_user = auth_provider.get_user(token)
        if google_user.get("email"):
            user_info = {
                "email": google_user.get("email"),
                "username": google_user.get("email"),
                "first_name": google_user.get("given_name"),
                "last_name": google_user.get("family_name"),
                "avatar_url": google_user.get("picture"),
            }

            return user_access(request, user_info, models.User.LOGIN_GOOGLE)
        else:
            raise oauth_providers.OauthException()
    except Exception as e:
        # print("%s (%s)" % (e.message, type(e)))
        return redirect(reverse("users:login"))


class LoginMethodNotMatch(Exception):
    pass


def user_access(request, user_info, login_method):
    try:
        user = models.User.objects.get(email=user_info["email"])
        if user.login_method != login_method:
            raise LoginMethodNotMatch()

        login(request, user)
        return redirect(reverse("core:home"))
    except models.User.DoesNotExist:
        user = models.User.objects.create(email=user_info["email"])
        for key, val in user_info.items():
            if key not in ["email", "avatar_url"]:
                setattr(user, key, val)
            user.login_method = login_method
            user.set_unusable_password()
            user.save()

        if user_info.get("avatar_url") is not None:
            avatar_request = requests.get(user_info.get("avatar_url"))
            user.avatar.save(
                f"{user.first_name}-avatar", ContentFile(avatar_request.content)
            )

        return user_access(request, user_info, models.User.LOGIN_GOOGLE)
