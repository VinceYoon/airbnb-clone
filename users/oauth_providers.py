import requests
from django.urls import reverse
from django.utils.http import urlencode
from django.conf import settings


class OauthProvider(object):
    def __init__(
        self,
        request,
        social_client,
        scope=None,
    ):
        self.request = request
        self.social_client = social_client
        self.scope = scope

    def set_auth_provider(self):
        if self.social_client:
            self.client_id = getattr(
                settings, f"{self.social_client.upper()}_CLIENT_ID", None
            )
            self.client_secret = getattr(
                settings, f"{self.social_client.upper()}_CLIENT_SECRET", None
            )
            self.redirect_uri = self.request.build_absolute_uri(
                reverse(f"users:{self.social_client}-callback")
            )

    def request_auth(self):
        self.set_auth_provider()
        auth_url = self.set_auth_url()
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": self.scope,
        }
        if self.extra_params:
            params.update(self.extra_params)

        return "%s?%s" % (
            auth_url,
            urlencode(params),
        )

    def set_auth_url(self):
        auth_url = getattr(settings, f"{self.social_client.upper()}_OAUTH", None)
        auth_url += "/authorize" if self.social_client == "github" else "/auth"
        return auth_url

    def set_access_token_url(self):
        access_token_url = getattr(
            settings, f"{self.social_client.upper()}_OAUTH", None
        )
        access_token_url += (
            "/access_token" if self.social_client == "github" else "/token"
        )

        return access_token_url

    def set_access_user_url(self):
        access_user_url = getattr(settings, f"{self.social_client.upper()}_USER", None)
        return access_user_url

    def set_access_token_params(self, code):
        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
        }

        if self.social_client == "google":
            params["redirect_uri"] = self.redirect_uri
            params["grant_type"] = "authorization_code"

        return params

    def get_access_token(self):
        code = self.request.GET.get("code", None)
        if code is not None:
            self.set_auth_provider()
            interface_headers = {"Accept": "application/json"}
            access_token_url = self.set_access_token_url()
            params = self.set_access_token_params(code)

            token_request = requests.post(
                access_token_url, headers=interface_headers, params=params
            )

            token_response = token_request.json()
            if not token_response.get("error"):
                return token_response.get("access_token")
            else:
                raise OauthException()
        else:
            raise OauthException()

    def set_interface_headers(self, token):
        interface_headers = {"Accept": "application/json"}
        interface_headers["Authorization"] = (
            f"token {token}"
            if self.social_client == "github"
            else f"access_token {token}"
        )
        return interface_headers

    def get_user(self, token, extra_context=None):
        interface_headers = self.set_interface_headers(token)
        access_user_url = self.set_access_user_url()
        if extra_context:
            access_user_url += extra_context

        user_request = (
            requests.get(access_user_url, headers=interface_headers)
            if self.social_client == "github"
            else requests.get(
                access_user_url,
                headers=interface_headers,
                params={"access_token": token},
            )
        )

        return user_request.json()


class OauthException(Exception):
    pass
