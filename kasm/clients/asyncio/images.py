from typing import TYPE_CHECKING

from kasm.clients.abc.images import ImageClientABC
from kasm.responses import ClientResponse

if TYPE_CHECKING:
    from kasm.clients.asyncio.clients import AsyncClient


class ImageAsyncClient(ImageClientABC):
    """Asynchronous implementation of `ImageClientABC` using `aiohttp`."""

    client: "AsyncClient"

    async def get(self) -> ClientResponse:
        """Retrieve a list of available images.

        Permission Required: `Images View`.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#get-images
        """
        return await self.client.post("get-images")
