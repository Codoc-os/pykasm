from kasm.clients import AsyncClient, SyncClient
from kasm.connections import async_connections, connections


class KasmObject:
    """Base class for all Kasm objects."""

    def __init__(self, using: str | None) -> None:
        self._using = using

    @staticmethod
    def _normalize_id(id_: str) -> str:
        """Normalize IDs between different endpoints.

        Some endpoints return IDs with dashes, while others do not. This method
        removes dashes from IDs to ensure consistency.
        """
        return id_.replace("-", "")

    def client(self, using: str | None = None) -> SyncClient:
        """Return the synchronous client associated with the object.

        It can be overridden with `using`.
        """
        return connections.get_connection(using or self._using)

    def async_client(self, using: str | None = None) -> AsyncClient:
        """Return the asynchronous client associated with the object.

        It can be overridden with `using`.
        """
        return async_connections.get_connection(using or self._using)
