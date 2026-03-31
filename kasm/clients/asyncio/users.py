from typing import TYPE_CHECKING

from kasm.clients.abc.users import UserClientABC
from kasm.responses import ClientResponse

if TYPE_CHECKING:
    from kasm.clients.asyncio.clients import AsyncClient


class UserAsyncClient(UserClientABC):
    """Asynchronous implementation of `UserClientABC` using `aiohttp`."""

    client: "AsyncClient"

    async def create(
        self,
        username: str,
        password: str,
        first_name: str | None,
        last_name: str | None,
        phone: str | None,
        organization: str | None,
        locked: bool = False,
        disabled: bool = False,
        raise_on_error: bool = True,
    ) -> ClientResponse:
        """Create a new user.

        Permission Required: `Users Create`.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#create-user
        """
        payload = {
            "target_user": {
                "username": username,
                "password": password,
                "first_name": first_name,
                "last_name": last_name,
                "phone": phone,
                "organization": organization,
                "locked": locked,
                "disabled": disabled,
            }
        }
        return await self.client.post("create-user", json=payload, raise_on_error=raise_on_error)

    async def get(self, *, user_id: str = None, username: str = None, raise_on_error: bool = True) -> ClientResponse:
        """Retrieve the properties of existing users.

        Target user's `user_id` or `username` can be passed to retrieve a
        specific user.

        Permission Required: `Users View`. Additionally, `Servers View` to
        receive assigned server information.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#get-user
        https://docs.kasm.com/docs/developers/developer_api#get-users.
        """
        if user_id is not None:
            return await self.client.post(
                "get-user", json={"target_user": {"user_id": user_id}}, raise_on_error=raise_on_error
            )
        if username is not None:
            return await self.client.post(
                "get-user", json={"target_user": {"username": username}}, raise_on_error=raise_on_error
            )
        return await self.client.post("get-users", raise_on_error=raise_on_error)

    async def update(
        self,
        user_id: str = None,
        username: str = None,
        password: str = None,
        first_name: str = None,
        last_name: str = None,
        phone: str = None,
        organization: str = None,
        locked: bool = None,
        disabled: bool = None,
        raise_on_error: bool = True,
    ) -> ClientResponse:
        """Update the properties of an existing user.

        Permission Required: `Users Modify` and `Users Modify Admin` to update
        users with Global Admin permission.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#update-user
        """
        payload = {
            "target_user": {k: v for k, v in locals().items() if v is not None and k not in ("self", "raise_on_error")}
        }
        return await self.client.post("update-user", json=payload, raise_on_error=raise_on_error)

    async def delete(self, user_id: str, force: bool = False, raise_on_error: bool = True) -> ClientResponse:
        """Delete an existing user.

        If the user has any existing Kasm sessions, deletion will fail. Set the
        `force` argument to `True` to delete the user's sessions and delete
        the user.

        Permission Required: `Users Delete` and `Users Modify`,
        `Users Modify Admin` is required to delete a user with Global Admin
        permission.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#delete-user
        """
        payload = {"target_user": {"user_id": user_id}, "force": force}
        return await self.client.post("delete-user", json=payload, raise_on_error=raise_on_error)

    async def logout(self, user_id: str, raise_on_error: bool = True) -> ClientResponse:
        """Logout all sessions for an existing user.

        Permission Required: `Users Auth Session`.

        For more information, see https://docs.kasm.com/docs/developers/developer_api#logout-user
        """
        payload = {"target_user": {"user_id": user_id}}
        return await self.client.post("logout-user", json=payload, raise_on_error=raise_on_error)

    async def get_attributes(self, user_id: str, raise_on_error: bool = True) -> ClientResponse:
        """Get the attribute (preferences) settings for an existing user.

        Permission Required: `Users View`.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#get-user-attributes
        """
        payload = {"target_user": {"user_id": user_id}}
        return await self.client.post("get-user-attributes", json=payload, raise_on_error=raise_on_error)

    async def update_attributes(
        self,
        user_id: str,
        ssh_public_key: str,
        show_tips: bool,
        theme: str,
        preferred_language: str,
        preferred_timezone: str,
        toggle_control_panel: bool,
        default_image: str | None,
        auto_login_kasm: bool | None,
        raise_on_error: bool = True,
    ) -> ClientResponse:
        """Update a user attributes.

        Permission Required: `Servers Modify` and `Users Modify`. Also
        `Users Modify Admin` if the target user has the Global Admin permission.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#update-user-attributes
        """
        payload = {
            "target_user_attributes": {
                "user_id": user_id,
                "ssh_public_key": ssh_public_key,
                "show_tips": show_tips,
                "theme": theme,
                "preferred_language": preferred_language,
                "preferred_timezone": preferred_timezone,
                "toggle_control_panel": toggle_control_panel,
                "default_image": default_image,
                "auto_login_kasm": auto_login_kasm,
            }
        }
        return await self.client.post("update-user-attributes", json=payload, raise_on_error=raise_on_error)

    async def add_to_group(self, user_id: str, group_id: str, raise_on_error: bool = True) -> ClientResponse:
        """Add a User to an existing Group.

        Permission Required: `Groups Modify`, `Groups Modify System` to add the
        user to the built-in All Users or Administrator groups.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#add-user-to-group
        """
        payload = {"target_user": {"user_id": user_id}, "target_group": {"group_id": group_id}}
        return await self.client.post("add-user-group", json=payload, raise_on_error=raise_on_error)

    async def remove_from_group(self, user_id: str, group_id: str, raise_on_error: bool = True) -> ClientResponse:
        """Remove a User from an existing Group.

        Permission Required: `Groups Modify`, `Groups Modify System` to remove
        the user from the built-in All Users or Administrator groups.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#remove-user-from-group
        """
        payload = {"target_user": {"user_id": user_id}, "target_group": {"group_id": group_id}}
        return await self.client.post("remove-user-group", json=payload, raise_on_error=raise_on_error)

    async def assign_server(self, user_id: str, server_id: str, raise_on_error: bool = True) -> ClientResponse:
        """Assign a User to a Server in a Server Pool.

        The relationship between User and Server is many-to-many.

        Permission Required: `Servers Modify` and `Users Modify`. Also
        `Users Modify Admin` if the target user has the Global Admin permission.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#assign-user-to-server
        """
        payload = {"target_user": {"user_id": user_id}, "target_server": {"server_id": server_id}}
        return await self.client.post("assign-user-server", json=payload, raise_on_error=raise_on_error)

    async def unassign_server(self, user_id: str, server_id: str, raise_on_error: bool = True) -> ClientResponse:
        """Unassigns a User from a Server in a Server Pool.

        Permission Required: `Servers Modify` and `Users Modify`. Also
        `Users Modify Admin` if the target user has the Global Admin permission.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#assign-user-to-server
        """
        payload = {"target_user": {"user_id": user_id}, "target_server": {"server_id": server_id}}
        return await self.client.post("unassign-user-server", json=payload, raise_on_error=raise_on_error)
