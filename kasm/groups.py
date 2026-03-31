from typing import TYPE_CHECKING

from kasm.abc import KasmObject

if TYPE_CHECKING:
    from kasm.users import User


class Group(KasmObject):
    """Represent a Kasm group."""

    def __init__(self, using: str | None, group_id: str, name: str) -> None:
        super().__init__(using)
        self.group_id = self._normalize_id(group_id)
        self.name = name

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.group_id} - {self.name}>"

    def add_user(self, user: "str | User", using: str | None = None) -> None:
        """Add a user to the group.

        Permission Required: `Groups Modify`, `Groups Modify System` to add the
        user to the built-in All Users or Administrator groups.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#add-user-to-group
        """
        from kasm.users import User

        if isinstance(user, User):
            user.add_to_group(self, using=using)
        else:
            self.client(using).users.add_to_group(user, self.group_id)

    async def aadd_user(self, user: "str | User", using: str | None = None) -> None:
        """Add a user to the group.

        Permission Required: `Groups Modify`, `Groups Modify System` to add the
        user to the built-in All Users or Administrator groups.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#add-user-to-group
        """
        from kasm.users import User

        if isinstance(user, User):
            await user.aadd_to_group(self, using=using)
        else:
            await self.async_client(using).users.add_to_group(user, self.group_id)

    def remove_user(self, user: "str | User", using: str | None = None) -> None:
        """Remove a user from the group.

        Permission Required: `Groups Modify`, `Groups Modify System` to remove
        the user from the built-in All Users or Administrator groups.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#remove-user-from-group
        """
        from kasm.users import User

        if isinstance(user, User):
            user.remove_from_group(self, using=using)
        else:
            self.client(using).users.remove_from_group(user, self.group_id)

    async def aremove_user(self, user: "str | User", using: str | None = None) -> None:
        """Remove a user from the group.

        Permission Required: `Groups Modify`, `Groups Modify System` to remove
        the user from the built-in All Users or Administrator groups.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#remove-user-from-group
        """
        from kasm.users import User

        if isinstance(user, User):
            await user.aremove_from_group(self, using=using)
        else:
            await self.async_client(using).users.remove_from_group(user, self.group_id)
