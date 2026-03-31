import abc
import functools
from typing import TYPE_CHECKING, Awaitable, Generic, TypeVar
from urllib.parse import urljoin

from kasm.clients.abc.clients import NamespacedClientABC
from kasm.responses import ClientResponse

if TYPE_CHECKING:
    from kasm.clients.abc.clients import ClientABC  # noqa: F401

C = TypeVar("C", bound="ClientABC")


class ImageClientABC(NamespacedClientABC[C], Generic[C]):
    """Base class for sub-client handling interaction with images."""

    @functools.cached_property
    def endpoints(self) -> dict[str, str]:
        """Return the endpoints used by the namespaced client."""
        return {
            "get-images": urljoin(self.client.url, "/api/public/get_images"),
        }

    @abc.abstractmethod
    def get(self) -> ClientResponse | Awaitable[ClientResponse]:
        """Retrieve a list of available images.

        Permission Required: `Images View`.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#get-images
        """
