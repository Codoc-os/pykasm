from typing import TYPE_CHECKING, Any, Self

from kasm.abc import KasmObject
from kasm.connections import async_connections, connections

if TYPE_CHECKING:
    from kasm.users import User


class Attribute(KasmObject):
    """Represent the attributes (preferences) for a Kasm user."""

    def __init__(
        self,
        using: str | None,
        user_attributes_id: str,
        user: "User",
        ssh_public_key: str,
        show_tips: bool,
        theme: str,
        preferred_language: str,
        preferred_timezone: str,
        toggle_control_panel: bool,
        default_image: str | None,
        auto_login_kasm: bool | None,
    ) -> None:
        super().__init__(using)
        self.user_attributes_id = self._normalize_id(user_attributes_id)
        self.user = user
        self.ssh_public_key = ssh_public_key
        self.show_tips = show_tips
        self.theme = theme
        self.preferred_language = preferred_language
        self.preferred_timezone = preferred_timezone
        self.toggle_control_panel = toggle_control_panel
        self.default_image = default_image
        self.auto_login_kasm = auto_login_kasm

    def __repr__(self) -> str:
        return f"<Attribute: {self.user!r}>"

    @classmethod
    def _from_response(cls, using: str | None, data: dict[str, Any], user: "User") -> Self:
        """Create an instance from the typical API response structure.

        `data` must be the dictionary containing the instance information, e.g.
            * `{ "user_attributes_id": "<id>", ...}`
        not
            * `{ "user_attributes": { "user_attributes_id": "<id>", ...}}`.
        """
        return cls(
            using=using,
            user_attributes_id=data["user_attributes_id"],
            user=user,
            ssh_public_key=data["ssh_public_key"],
            show_tips=data["show_tips"],
            theme=data["theme"],
            preferred_language=data["preferred_language"],
            preferred_timezone=data["preferred_timezone"],
            toggle_control_panel=data["toggle_control_panel"],
            default_image=data["default_image"],
            auto_login_kasm=data["auto_login_kasm"],
        )

    @classmethod
    def get(cls, user: "User", using: str | None = None) -> Self:
        """Get the attribute (preferences) settings for the user.

        Permission Required: `Users View`.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#get-user-attributes
        """
        data = connections.get_connection(using).users.get_attributes(user.user_id).json()
        return cls._from_response(using, data["user_attributes"], user)

    @classmethod
    async def aget(cls, user: "User", using: str | None = None) -> Self:
        """Get the attribute (preferences) settings for the user.

        Permission Required: `Users View`.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#get-user-attributes
        """
        data = (await async_connections.get_connection(using).users.get_attributes(user.user_id)).json()
        return cls._from_response(using, data["user_attributes"], user)

    def refresh(self) -> Self:
        """Refresh the instance data from the API."""
        return self.get(user=self.user)

    async def arefresh(self) -> Self:
        """Refresh the instance data from the API."""
        return await self.aget(user=self.user)

    def save(self, using: str | None = None) -> Self:
        """Save the user attributes.

        Permission Required: `Servers Modify` and `Users Modify`. Also
        `Users Modify Admin` if the target user has the Global Admin permission.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#update-user-attributes
        """
        self.client(using).users.update_attributes(
            user_id=self.user.user_id,
            ssh_public_key=self.ssh_public_key,
            show_tips=self.show_tips,
            theme=self.theme,
            preferred_language=self.preferred_language,
            preferred_timezone=self.preferred_timezone,
            toggle_control_panel=self.toggle_control_panel,
            default_image=self.default_image,
            auto_login_kasm=self.auto_login_kasm,
        )
        return self

    async def asave(self, using: str | None = None) -> Self:
        """Save the user attributes.

        Permission Required: `Servers Modify` and `Users Modify`. Also
        `Users Modify Admin` if the target user has the Global Admin permission.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#update-user-attributes
        """
        await self.async_client(using).users.update_attributes(
            user_id=self.user.user_id,
            ssh_public_key=self.ssh_public_key,
            show_tips=self.show_tips,
            theme=self.theme,
            preferred_language=self.preferred_language,
            preferred_timezone=self.preferred_timezone,
            toggle_control_panel=self.toggle_control_panel,
            default_image=self.default_image,
            auto_login_kasm=self.auto_login_kasm,
        )
        return self
