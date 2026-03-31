import abc
import functools
from typing import TYPE_CHECKING, Awaitable, Generic, TypeVar
from urllib.parse import urljoin

from kasm.clients.abc.clients import NamespacedClientABC
from kasm.responses import ClientResponse

if TYPE_CHECKING:
    from kasm.clients.abc.clients import ClientABC  # noqa: F401

C = TypeVar("C", bound="ClientABC")


class UserClientABC(NamespacedClientABC[C], Generic[C]):
    """Base class for sub-client handling interaction with users."""

    @functools.cached_property
    def endpoints(self) -> dict[str, str]:
        """Return the endpoints used by the namespaced client."""
        return {
            "create-user": urljoin(self.client.url, "/api/public/create_user"),
            "get-user": urljoin(self.client.url, "/api/public/get_user"),
            "get-users": urljoin(self.client.url, "/api/public/get_users"),
            "update-user": urljoin(self.client.url, "/api/public/update_user"),
            "delete-user": urljoin(self.client.url, "/api/public/delete_user"),
            "logout-user": urljoin(self.client.url, "/api/public/logout_user"),
            "get-user-attributes": urljoin(self.client.url, "/api/public/get_attributes"),
            "update-user-attributes": urljoin(self.client.url, "/api/public/update_user_attributes"),
            "add-user-group": urljoin(self.client.url, "/api/public/add_user_group"),
            "remove-user-group": urljoin(self.client.url, "/api/public/remove_user_group"),
            "assign-user-server": urljoin(self.client.url, "/api/public/assign_user_server"),
            "unassign-user-server": urljoin(self.client.url, "/api/public/unassign_user_server"),
        }

    @abc.abstractmethod
    def create(
        self,
        username: str,
        password: str,
        first_name: str,
        last_name: str,
        phone: str,
        organization: str,
        locked: bool = False,
        disabled: bool = False,
        raise_on_error: bool = True,
    ) -> ClientResponse | Awaitable[ClientResponse]:
        """Create a new user.

        Permission Required: `Users Create`.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#create-user
        """

    @abc.abstractmethod
    def get(
        self, *, user_id: str = None, username: str = None, raise_on_error: bool = True
    ) -> ClientResponse | Awaitable[ClientResponse]:
        """Retrieve the properties of existing users.

        Target user's `user_id` or `username` can be passed to retrieve a
        specific user.

        Permission Required: `Users View`. Additionally, `Servers View` to
        receive assigned server information.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#get-user
        https://docs.kasm.com/docs/developers/developer_api#get-users.
        """

    @abc.abstractmethod
    def update(
        self,
        user_id: str,
        username: str,
        password: str,
        first_name: str,
        last_name: str,
        phone: str,
        organization: str,
        locked: bool = False,
        disabled: bool = False,
        raise_on_error: bool = True,
    ) -> ClientResponse | Awaitable[ClientResponse]:
        """Update the properties of an existing user.

        Permission Required: `Users Modify` and `Users Modify Admin` to update
        users with Global Admin permission.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#update-user
        """

    @abc.abstractmethod
    def delete(
        self, user_id: str, force: bool = False, raise_on_error: bool = True
    ) -> ClientResponse | Awaitable[ClientResponse]:
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

    @abc.abstractmethod
    def logout(self, user_id: str, raise_on_error: bool = True) -> ClientResponse | Awaitable[ClientResponse]:
        """Logout all sessions for an existing user.

        Permission Required: `Users Auth Session`.

        For more information, see https://docs.kasm.com/docs/developers/developer_api#logout-user
        """

    @abc.abstractmethod
    def get_attributes(self, user_id: str, raise_on_error: bool = True) -> ClientResponse | Awaitable[ClientResponse]:
        """Get the attribute (preferences) settings for an existing user.

        Permission Required: `Users View`.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#get-user-attributes
        """

    @abc.abstractmethod
    def update_attributes(
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
    ) -> ClientResponse | Awaitable[ClientResponse]:
        """Update a user attributes.

        Permission Required: `Servers Modify` and `Users Modify`. Also
        `Users Modify Admin` if the target user has the Global Admin permission.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#update-user-attributes
        """

    @abc.abstractmethod
    def add_to_group(
        self, user_id: str, group_id: str, raise_on_error: bool = True
    ) -> ClientResponse | Awaitable[ClientResponse]:
        """Add a User to an existing Group.

        Permission Required: `Groups Modify`, `Groups Modify System` to add the
        user to the built-in All Users or Administrator groups.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#add-user-to-group
        """

    @abc.abstractmethod
    def remove_from_group(
        self, user_id: str, group_id: str, raise_on_error: bool = True
    ) -> ClientResponse | Awaitable[ClientResponse]:
        """Remove a User from an existing Group.

        Permission Required: `Groups Modify`, `Groups Modify System` to remove
        the user from the built-in All Users or Administrator groups.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#remove-user-from-group
        """

    @abc.abstractmethod
    def assign_server(
        self, user_id: str, server_id: str, raise_on_error: bool = True
    ) -> ClientResponse | Awaitable[ClientResponse]:
        """Assign a User to a Server in a Server Pool.

        The relationship between User and Server is many-to-many.

        Permission Required: `Servers Modify` and `Users Modify`. Also
        `Users Modify Admin` if the target user has the Global Admin permission.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#assign-user-to-server
        """

    @abc.abstractmethod
    def unassign_server(
        self, user_id: str, server_id: str, raise_on_error: bool = True
    ) -> ClientResponse | Awaitable[ClientResponse]:
        """Unassigns a User from a Server in a Server Pool.

        Permission Required: `Servers Modify` and `Users Modify`. Also
        `Users Modify Admin` if the target user has the Global Admin permission.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#assign-user-to-server
        """
