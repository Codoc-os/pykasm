import copy
from typing import Any, Generic, Type, TypeVar

from kasm.clients import AsyncClient, SyncClient
from kasm.clients.abc.clients import ClientABC

Client = TypeVar("Client", bound=ClientABC)


class Connections(Generic[Client]):
    """Holds connections to different Kasm API."""

    def __init__(self, client_class: Type[Client]) -> None:
        self._client_class = client_class
        self._client: dict[str, Client] = {}

    def __getitem__(self, alias: str) -> Client:
        return self._client[alias]

    def __setitem__(self, alias: str, client: Client) -> None:
        self._client[alias] = client

    def __delitem__(self, alias: str) -> None:
        del self._client[alias]

    def configure(self, **kwargs: Any) -> None:
        """Configure multiple clients at once.

        Useful for passing in config dictionaries obtained from other sources,
        like Django's settings or a configuration management tool.

        Examples
        --------
        ```python
        connections.configure(
            default={
                'scheme': 'http',
                'host': 'localhost'
                'port': 80,
                'prefix': 'api',
                'key': 'foo',
                'secret': 'bar'
            },
            test={
                'scheme': 'http',
                'host': 'localhost',
                'port': 5678,
                'prefix': 'test',
                'key': 'foo',
                'secret': 'bar',
            }
        )

        # Or using a dict
        config = {
            'default': {
                'scheme': 'http',
                'host': 'localhost'
                'port': 80,
                'prefix': 'api',
                'key': 'foo',
                'secret': 'bar'
            },
            'test': {
                'scheme': 'http',
                'host': 'localhost',
                'port': 5678,
                'prefix': 'test',
                'id': 1,
                'key': 'foo',
                'secret': 'bar',
            }
        }
        connections.configure(**config)
        ```
        """
        for k, v in kwargs.items():
            self.create_connection(k, **v)

    def create_connection(self, alias: str, **kwargs: Any) -> Any:
        """Create a client and register it under given alias."""
        client = self._client[alias] = self._client_class(**kwargs)
        return client

    def get_connection(self, alias: str = None) -> Client:
        """Return the client corresponding to alias."""
        return self._client[alias or "default"]

    add_connection = __setitem__

    remove_connection = __delitem__


# Using a global instances holding all the connections allows to easily reuse
# them across an application.
connections: Connections[SyncClient] = Connections(SyncClient)
async_connections: Connections[AsyncClient] = Connections(AsyncClient)


def configure(**kwargs: Any) -> None:  # pragma: no cover
    """Configure both the synchronous and asynchronous clients."""
    connections.configure(**copy.deepcopy(kwargs))
    async_connections.configure(**kwargs)
