from typing import TYPE_CHECKING

from kasm.clients.abc.images import ImageClientABC
from kasm.responses import ClientResponse

if TYPE_CHECKING:
    from kasm.clients.sync.clients import SyncClient


class ImageSyncClient(ImageClientABC):
    """Synchronous implementation of `ImageClientABC` using `requests`."""

    client: "SyncClient"

    def get(self) -> ClientResponse:
        """Retrieve a list of available images.

        Permission Required: `Images View`.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#get-images
        """
        return self.client.post("get-images")
