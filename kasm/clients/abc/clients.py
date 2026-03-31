import abc
import functools
import operator
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from kasm.clients.abc.images import ImageClientABC
    from kasm.clients.abc.sessions import SessionClientABC
    from kasm.clients.abc.users import UserClientABC

C = TypeVar("C", bound="ClientABC")


class NamespacedClientABC(abc.ABC, Generic[C]):
    """Base class for specific namespaced clients of `ClientABC`."""

    def __init__(self, client: C) -> None:
        self.client = client

    @property
    @abc.abstractmethod
    def endpoints(self) -> dict[str, str]:
        """Return the endpoints used by the namespaced client."""


class ClientABC(abc.ABC):
    """Base class for client handling communication with the Kasm API."""

    images: "ImageClientABC"
    sessions: "SessionClientABC"
    users: "UserClientABC"

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

        match (url, scheme, host, port, prefix):
            case (str(), _, None, _, _):
                self.url = url
            case (None, str(), str(), _, str()):
                port = f":{port}" if port else ""
                self.url = f"{scheme}://{host}{port}{prefix}"
            case _:
                raise ValueError("You must provide either `url`, or `scheme`, `host`, `port` and `prefix`.")

        self.key = key
        self.secret = secret
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.allow_redirects = allow_redirects

    def __hash__(self) -> int:
        return hash((self.url, self.key, self.secret, self.timeout, self.verify_ssl, self.allow_redirects))

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and hash(self) == hash(other)

    @functools.cached_property
    def endpoints(self) -> dict[str, str]:
        """Reduce all namespaced client endpoints into a single dict."""
        return functools.reduce(
            operator.or_, [c.endpoints for c in self.__dict__.values() if isinstance(c, NamespacedClientABC)]
        )
