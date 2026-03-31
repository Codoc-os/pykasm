import json
from typing import Any, Mapping

import aiohttp
import requests


class ClientResponse:
    """Common interface for responses from the clients."""

    def __init__(self, url: str, status_code: int, content: bytes, headers: Mapping[str, str]) -> None:
        self.url = url
        self.status_code = status_code
        self.content = content
        self.headers = headers

    @classmethod
    def from_requests(cls, response: requests.Response) -> "ClientResponse":
        """Create a Response from a requests.Response."""
        return cls(response.url, response.status_code, response.content, response.headers)

    @classmethod
    async def from_aiohttp(cls, response: aiohttp.ClientResponse) -> "ClientResponse":
        """Create a Response from a aiohttp.ClientResponse."""
        return cls(str(response.url), response.status, await response.read(), response.headers)

    def json(self) -> dict[str, Any]:
        """Return the content as a json."""
        return json.loads(self.content.decode())

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} [{self.status_code}]>"

    __str__ = __repr__
