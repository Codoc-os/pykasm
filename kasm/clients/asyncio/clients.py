from typing import Any, Literal

import aiohttp

from kasm.clients.abc.clients import ClientABC
from kasm.clients.asyncio.images import ImageAsyncClient
from kasm.clients.asyncio.sessions import SessionAsyncClient
from kasm.clients.asyncio.users import UserAsyncClient
from kasm.exceptions import RequestError
from kasm.responses import ClientResponse


class AsyncClient(ClientABC):
    """Asynchronous implementation of `ClientABC` using `aiohttp`."""

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
        self.timeout: aiohttp.ClientTimeout = aiohttp.ClientTimeout(timeout)
        self.images: ImageAsyncClient = ImageAsyncClient(self)
        self.sessions: SessionAsyncClient = SessionAsyncClient(self)
        self.users: UserAsyncClient = UserAsyncClient(self)

    async def _request(
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
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method, url, **kwargs, timeout=self.timeout, ssl=self.verify_ssl, allow_redirects=self.allow_redirects
            ) as response:
                wrapped = await ClientResponse.from_aiohttp(response)
        if wrapped.status_code >= 300 and raise_on_error:
            raise RequestError(wrapped)
        return wrapped

    async def get(self, endpoint: str, raise_on_error: bool = True, **kwargs: Any) -> ClientResponse:
        """Make a GET request to Kasm API."""
        return await self._request("get", endpoint, raise_on_error=raise_on_error, **kwargs)

    async def post(self, endpoint: str, raise_on_error: bool = True, **kwargs: Any) -> ClientResponse:
        """Make a POST request to Kasm API."""
        return await self._request("post", endpoint, raise_on_error=raise_on_error, **kwargs)

    async def delete(self, endpoint: str, raise_on_error: bool = True, **kwargs: Any) -> ClientResponse:
        """Make a DELETE request to Kasm API."""
        return await self._request("delete", endpoint, raise_on_error=raise_on_error, **kwargs)
