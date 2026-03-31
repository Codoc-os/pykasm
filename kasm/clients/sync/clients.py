from typing import Any, Literal

import requests

from kasm.clients.abc.clients import ClientABC
from kasm.clients.sync.images import ImageSyncClient
from kasm.clients.sync.sessions import SessionSyncClient
from kasm.clients.sync.users import UserSyncClient
from kasm.exceptions import RequestError
from kasm.responses import ClientResponse


class SyncClient(ClientABC):
    """Synchronous implementation of `ClientABC` using `requests`."""

    def __init__(
        self,
        key: str,
        secret: str,
        url: str = None,
        scheme: str = "http",
        host: str = None,
        port: str | int = None,
        prefix: str = "/",
        timeout: int = 30,
        verify_ssl: bool = True,
        allow_redirects: bool = False,
    ) -> None:
        super().__init__(key, secret, url, scheme, host, port, prefix, timeout, verify_ssl, allow_redirects)
        self.images: ImageSyncClient = ImageSyncClient(self)
        self.sessions: SessionSyncClient = SessionSyncClient(self)
        self.users: UserSyncClient = UserSyncClient(self)

    def _request(
        self,
        method: Literal["get", "post", "delete", "put", "patch", "options"],
        endpoint: str,
        raise_on_error: bool = True,
        **kwargs: Any,
    ) -> ClientResponse:
        url = self.endpoints[endpoint]
        kwargs["headers"] = {"Accept": "application/json", "Content-Type": "application/json"} | kwargs.get(
            "headers", {}
        )
        kwargs["json"] = kwargs.get("json", {}) | {"api_key": self.key, "api_key_secret": self.secret}

        response = ClientResponse.from_requests(
            requests.request(
                method,
                url,
                **kwargs,
                timeout=self.timeout,
                verify=self.verify_ssl,
                allow_redirects=self.allow_redirects,
            )
        )
        if response.status_code >= 300 and raise_on_error:
            raise RequestError(response)
        return response

    def get(self, endpoint: str, raise_on_error: bool = True, **kwargs: Any) -> ClientResponse:
        """Make a GET request to Kasm API."""
        return self._request("get", endpoint, raise_on_error=raise_on_error, **kwargs)

    def post(self, endpoint: str, raise_on_error: bool = True, **kwargs: Any) -> ClientResponse:
        """Make a POST request to Kasm API."""
        return self._request("post", endpoint, raise_on_error=raise_on_error, **kwargs)

    def delete(self, endpoint: str, raise_on_error: bool = True, **kwargs: Any) -> ClientResponse:
        """Make a DELETE request to Kasm API."""
        return self._request("delete", endpoint, raise_on_error=raise_on_error, **kwargs)
