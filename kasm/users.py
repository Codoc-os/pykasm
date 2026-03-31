import datetime
from typing import TYPE_CHECKING, Any, Self

from kasm.abc import KasmObject
from kasm.attributes import Attribute
from kasm.connections import async_connections, connections
from kasm.groups import Group

if TYPE_CHECKING:
    from kasm.sessions import Session


class User(KasmObject):
    """Represent a Kasm user."""

    def __init__(
        self,
        using: str | None,
        user_id: str,
        username: str,
        first_name: str | None = None,
        last_name: str | None = None,
        phone: str | None = None,
        email: str | None = None,
        notes: str | None = None,
        realm: str | None = None,
        organization: str | None = None,
        city: str | None = None,
        state: str | None = None,
        country: str | None = None,
        locked: bool | None = None,
        disabled: bool | None = None,
        two_factor: bool | None = None,
        created: datetime.datetime | None = None,
        password_set_date: datetime.datetime | None = None,
        last_session: datetime.datetime | None = None,
        program_id: str | None = None,
        groups: list[Group] | None = None,
        sessions: list[dict[str, Any]] | None = None,
        assigned_servers: list | None = None,
    ) -> None:
        super().__init__(using)
        self.user_id = self._normalize_id(user_id)
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.notes = notes
        self.realm = realm
        self.organization = organization
        self.city = city
        self.state = state
        self.country = country
        self.locked = locked
        self.disabled = disabled
        self.two_factor = two_factor
        self.created = created
        self.password_set_date = password_set_date
        self.last_session = last_session
        self.program_id = program_id
        self.groups = groups or []
        self._sessions_lazy: list[dict[str, Any]] = sessions or []
        self._sessions: list["Session"] | None = None
        self.assigned_servers = assigned_servers or []
        self._attributes: Attribute | None = None

    def __repr__(self) -> str:
        return f"<User: {self.user_id} - {self.username}>"

    @property
    def attributes(self) -> Attribute:
        """Lazy-load the user's attributes."""
        if self._attributes is None:
            self._attributes = Attribute.get(self, using=self._using)
        return self._attributes

    @property
    def sessions(self) -> list["Session"]:
        """Lazy-load the user's sessions."""
        from kasm.sessions import Session

        if self._sessions is None:
            self._sessions = [Session(self._using, s["kasm_id"], self).update_status() for s in self._sessions_lazy]
        return self._sessions

    @classmethod
    def _from_response(cls, using: str | None, data: dict[str, Any]) -> Self:
        """Create an instance from the typical API response structure.

        `data` must be the dictionary containing the instance information, e.g.
            * `{ "user_id": "<id>", ...}`
        not
            * `{ "user": { "user_id": "<id>", ...}}`.
        """
        groups = [Group(using=using, group_id=g["group_id"], name=g["name"]) for g in data.get("groups", [])]
        if data.get("created") == "None":
            data["created"] = None
        if data.get("password_set_date") == "None":
            data["password_set_date"] = None
        if data.get("last_session") == "None":
            data["last_session"] = None
        return cls(
            using=using,
            user_id=data["user_id"],
            username=data["username"],
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            phone=data.get("phone"),
            email=data.get("email"),
            notes=data.get("notes"),
            realm=data.get("realm"),
            organization=data.get("organization"),
            city=data.get("city"),
            state=data.get("state"),
            country=data.get("country"),
            locked=data.get("locked"),
            disabled=data.get("disabled"),
            two_factor=data.get("two_factor"),
            created=data.get("created") and datetime.datetime.fromisoformat(data["created"]),
            password_set_date=(
                data.get("password_set_date") and datetime.datetime.fromisoformat(data["password_set_date"])
            ),
            last_session=data.get("last_session") and datetime.datetime.fromisoformat(data["last_session"]),
            program_id=data.get("program_id"),
            groups=groups,
            sessions=data.get("kasms"),
            assigned_servers=data.get("assigned_servers"),
        )

    @classmethod
    def create(
        cls,
        username: str,
        password: str,
        first_name: str | None = None,
        last_name: str | None = None,
        phone: str | None = None,
        organization: str | None = None,
        locked: bool = False,
        disabled: bool = False,
        using: str | None = None,
    ) -> Self:
        """Create a new user.

        Permission Required: `Users Create`.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#create-user
        """
        data = (
            connections.get_connection(using)
            .users.create(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                organization=organization,
                locked=locked,
                disabled=disabled,
            )
            .json()
        )
        return cls._from_response(using, data["user"])

    @classmethod
    async def acreate(
        cls,
        username: str,
        password: str,
        first_name: str | None = None,
        last_name: str | None = None,
        phone: str | None = None,
        organization: str | None = None,
        locked: bool = False,
        disabled: bool = False,
        using: str | None = None,
    ) -> Self:
        """Create a new user.

        Permission Required: `Users Create`.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#create-user
        """
        data = (
            await async_connections.get_connection(using).users.create(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                organization=organization,
                locked=locked,
                disabled=disabled,
            )
        ).json()
        return cls._from_response(using, data["user"])

    @classmethod
    def get(cls, *, user_id: str | None = None, username: str | None = None, using: str | None = None) -> Self:
        """Retrieve a specific user.

        Permission Required: `Users View`. Additionally, `Servers View` to
        receive assigned server information.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#get-user
        """
        if user_id is None and username is None:
            raise ValueError("Either 'user_id' or 'username' must be provided.")
        data = connections.get_connection(using).users.get(user_id=user_id, username=username).json()
        return cls._from_response(using, data["user"])

    @classmethod
    async def aget(cls, user_id: str | None = None, username: str | None = None, using: str | None = None) -> Self:
        """Retrieve a specific user.

        Permission Required: `Users View`. Additionally, `Servers View` to
        receive assigned server information.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#get-user
        """
        if user_id is None and username is None:
            raise ValueError("Either 'user_id' or 'username' must be provided.")
        data = (await async_connections.get_connection(using).users.get(user_id=user_id, username=username)).json()
        return cls._from_response(using, data["user"])

    @classmethod
    def all(cls, using: str | None = None) -> list[Self]:
        """Retrieve all users.

        Permission Required: `Users View`. Additionally, `Servers View` to
        receive assigned server information.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#get-users.
        """
        data = connections.get_connection(using).users.get().json()
        users = []
        for user in data["users"]:
            users.append(cls._from_response(using, user))
        return users

    @classmethod
    async def aall(cls, using: str | None = None) -> list[Self]:
        """Retrieve all users.

        Permission Required: `Users View`. Additionally, `Servers View` to
        receive assigned server information.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#get-users.
        """
        data = (await async_connections.get_connection(using).users.get()).json()
        users = []
        for user in data["users"]:
            users.append(cls._from_response(using, user))
        return users

    def refresh(self) -> Self:
        """Refresh the instance data from the API."""
        return self.get(user_id=self.user_id)

    async def arefresh(self) -> Self:
        """Refresh the instance data from the API."""
        return await self.aget(user_id=self.user_id)

    def save(self, using: str | None = None) -> Self:
        """Save the user and its attributes.

        Permission Required: `Users Modify` and `Users Modify Admin` to update
        users with Global Admin permission.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#update-user
        """
        self.client(using).users.update(
            user_id=self.user_id,
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
            phone=self.phone,
            organization=self.organization,
            locked=self.locked,
            disabled=self.disabled,
        )
        if self._attributes is not None:
            self.attributes.save(using)
        return self

    async def asave(self, using: str | None = None) -> Self:
        """Save the user and its attributes.

        Permission Required: `Users Modify` and `Users Modify Admin` to update
        users with Global Admin permission.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#update-user
        """
        await self.async_client(using).users.update(
            user_id=self.user_id,
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
            phone=self.phone,
            organization=self.organization,
            locked=self.locked,
            disabled=self.disabled,
        )
        if self._attributes is not None:
            await self.attributes.asave(using)
        return self

    def set_password(self, password: str, using: str | None = None) -> Self:
        """Set the user's password.

        Permission Required: `Users Modify` and `Users Modify Admin` to update
        users with Global Admin permission.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#update-user
        """
        self.client(using).users.update(self.user_id, username=self.username, password=password)
        return self

    async def aset_password(self, password: str, using: str | None = None) -> Self:
        """Set the user's password.

        Permission Required: `Users Modify` and `Users Modify Admin` to update
        users with Global Admin permission.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#update-user
        """
        await self.async_client(using).users.update(self.user_id, username=self.username, password=password)
        return self

    def delete(self, force: bool = False, using: str | None = None) -> None:
        """Delete the user.

        If the user has any existing Kasm sessions, deletion will fail. Set the
        `force` argument to `True` to delete the user's sessions and delete
        the user.

        Permission Required: `Users Delete` and `Users Modify`,
        `Users Modify Admin` is required to delete a user with Global Admin
        permission.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#delete-user
        """
        self.client(using).users.delete(self.user_id, force=force)

    async def adelete(self, force: bool = False, using: str | None = None) -> None:
        """Delete the user.

        If the user has any existing Kasm sessions, deletion will fail. Set the
        `force` argument to `True` to delete the user's sessions and delete
        the user.

        Permission Required: `Users Delete` and `Users Modify`,
        `Users Modify Admin` is required to delete a user with Global Admin
        permission.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#delete-user
        """
        await self.async_client(using).users.delete(self.user_id, force=force)

    def logout(self, using: str | None = None) -> Self:
        """Logout all sessions for the user.

        Permission Required: `Users Auth Session`.

        For more information, see https://docs.kasm.com/docs/developers/developer_api#logout-user
        """
        self.client(using).users.logout(self.user_id)
        return self

    async def alogout(self, using: str | None = None) -> Self:
        """Logout all sessions for an existing user.

        Permission Required: `Users Auth Session`.

        For more information, see https://docs.kasm.com/docs/developers/developer_api#logout-user
        """
        await self.async_client(using).users.logout(self.user_id)
        return self

    def add_to_group(self, group: str | Group, using: str | None = None) -> Self:
        """Add the user to a group.

        Permission Required: `Users Modify` and `Groups Modify`. Also
        `Users Modify Admin` if the target user has the Global Admin permission
        or if adding to a group with the Global Admin permission.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#add-user-to-group
        """
        group_id = group.group_id if isinstance(group, Group) else group
        self.client(using).users.add_to_group(self.user_id, group_id)
        if isinstance(group, Group):
            self.groups.append(group)
        else:
            data = self.client(using).users.get(user_id=self.user_id).json()
            self.groups = [
                Group(using=using, group_id=g["group_id"], name=g["name"]) for g in data["user"].get("groups", [])
            ]
        return self

    async def aadd_to_group(self, group: str | Group, using: str | None = None) -> Self:
        """Add the user to a group.

        Permission Required: `Users Modify` and `Groups Modify`. Also
        `Users Modify Admin` if the target user has the Global Admin permission
        or if adding to a group with the Global Admin permission.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#add-user-to-group
        """
        group_id = group.group_id if isinstance(group, Group) else group
        await self.async_client(using).users.add_to_group(self.user_id, group_id)
        if isinstance(group, Group):
            self.groups.append(group)
        else:
            data = (await self.async_client(using).users.get(user_id=self.user_id)).json()
            self.groups = [
                Group(using=using, group_id=g["group_id"], name=g["name"]) for g in data["user"].get("groups", [])
            ]
        return self

    def remove_from_group(self, group: str | Group, using: str | None = None) -> Self:
        """Remove the user from a group.

        Permission Required: `Groups Modify`, `Groups Modify System` to remove
        the user from the built-in All Users or Administrator groups.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#remove-user-from-group
        """
        group_id = group.group_id if isinstance(group, Group) else group
        self.client(using).users.remove_from_group(self.user_id, group_id)
        if isinstance(group, Group):
            self.groups = [g for g in self.groups if g.group_id != group_id]
        else:
            data = self.client(using).users.get(user_id=self.user_id).json()
            self.groups = [
                Group(using=using, group_id=g["group_id"], name=g["name"]) for g in data["user"].get("groups", [])
            ]
        return self

    async def aremove_from_group(self, group: str | Group, using: str | None = None) -> Self:
        """Remove the user from a group.

        Permission Required: `Groups Modify`, `Groups Modify System` to remove
        the user from the built-in All Users or Administrator groups.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#remove-user-from-group
        """
        group_id = group.group_id if isinstance(group, Group) else group
        await self.async_client(using).users.remove_from_group(self.user_id, group_id)
        if isinstance(group, Group):
            self.groups = [g for g in self.groups if g.group_id != group_id]
        else:
            data = (await self.async_client(using).users.get(user_id=self.user_id)).json()
            self.groups = [
                Group(using=using, group_id=g["group_id"], name=g["name"]) for g in data["user"].get("groups", [])
            ]
        return self

    def assign_server(self, server_id: str, using: str | None = None) -> Self:
        """Assign a server to the user.

        Permission Required: `Servers Modify` and `Users Modify`. Also
        `Users Modify Admin` if the target user has the Global Admin permission.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#assign-user-to-server
        """
        self.client(using).users.assign_server(self.user_id, server_id)
        return self

    async def aassign_server(self, server_id: str, using: str | None = None) -> Self:
        """Assign a server to the user.

        Permission Required: `Servers Modify` and `Users Modify`. Also
        `Users Modify Admin` if the target user has the Global Admin permission.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#assign-user-to-server
        """
        await self.async_client(using).users.assign_server(self.user_id, server_id)
        return self

    def unassign_server(self, server_id: str, using: str | None = None) -> Self:
        """Unassign a server from the user.

        Permission Required: `Servers Modify` and `Users Modify`. Also
        `Users Modify Admin` if the target user has the Global Admin permission.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#assign-user-to-server
        """
        self.client(using).users.unassign_server(self.user_id, server_id)
        return self

    async def aunassign_server(self, server_id: str, using: str | None = None) -> Self:
        """Unassign a server from the user.

        Permission Required: `Servers Modify` and `Users Modify`. Also
        `Users Modify Admin` if the target user has the Global Admin permission.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#assign-user-to-server
        """
        await self.async_client(using).users.unassign_server(self.user_id, server_id)
        return self
