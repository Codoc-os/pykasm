from kasm.responses import ClientResponse


class KasmAPIError(Exception):
    """Base class for all exceptions raised by `kasm`."""


class RequestError(KasmAPIError):
    """Raised when a request to Kasm fails."""

    def __init__(self, response: ClientResponse, message: str = None) -> None:
        self.response = response
        self.message = message or "Request to '{url}' failed with status code '{status_code}':\n{content}"

    def __str__(self) -> str:
        return self.message.format(
            url=self.response.url, status_code=self.response.status_code, content=self.response.content
        )
