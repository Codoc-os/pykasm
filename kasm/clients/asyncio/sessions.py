from typing import TYPE_CHECKING, Any

from kasm.clients.abc.sessions import SessionClientABC
from kasm.enums import PersistentProfileMode, RdpClientType
from kasm.responses import ClientResponse

if TYPE_CHECKING:
    from kasm.clients.asyncio.clients import AsyncClient


class SessionAsyncClient(SessionClientABC):
    """Asynchronous implementation of `SessionClientABC` using `aiohttp`."""

    client: "AsyncClient"

    async def request(
        self,
        user_id: str,
        image_id: str,
        enable_sharing: bool = False,
        kasm_url: str = None,
        environment: dict[str, str] = None,
        connection_info: dict[str, str] = None,
        client_language: str = None,
        client_timezone: str = None,
        egress_gateway_id: str = None,
        persistent_profile_mode: PersistentProfileMode = None,
        rdp_client_type: RdpClientType = None,
        server_id: str = None,
        raise_on_error: bool = True,
    ) -> ClientResponse:
        """Request a new session to be created.

        Use `status()` to ensure the session reaches a running state,
        before directing the user to the session.

        Permission Required: `Users Auth Session` and `User`.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#request-kasm

        Parameters
        ----------
        user_id: str
            If specified, the Kasm session will be created under this user.
        image_id: str
            The ID of the image to use for the Kasm session.
        enable_sharing: bool, optional
            If set to `True`, the Kasm session will be created with sharing mode
            enabled by default. Default to `False`.
        kasm_url: str, optional
            If specified, the browser inside the session will navigate to this
            URL. Only applicable to browser-based images (e.g., Kasm Chrome,
            Firefox, Tor Browser).
        environment: dict[str, str], optional
            Environment variables to inject into the created container session.
        connection_info: dict[str, str], optional
            Custom RDP/VNC/SSH connection settings. Not applicable for
            container-based sessions.
        client_language: str, optional
            Language to be passed as an environment variable to the Kasm
            session. Refer to "Valid Languages" documentation for accepted
            values.
        client_timezone: str, optional
            Timezone to be passed as an environment variable to the Kasm
            session. Refer to "Valid Timezones" documentation for accepted
            values.
        egress_gateway_id: str, optional
            ID of the Egress Gateway the session should connect to at launch.
            The user must have permission and an associated Egress Credential.
            Only applies to container-based sessions. See the Egress
            documentation for details.
        persistent_profile_mode: PersistentProfileMode, optional
            Controls behavior of persistent profiles (only for container
            sessions with persistent profile path configured).
            - ENABLED: Uses a persistent profile. If it doesn't exist, it will be created.
            - DISABLED: Does not load a persistent profile.
            - RESET: Deletes any existing profile and creates a new one.
        rdp_client_type: RdpClientType, optional
            Required when the Workspace image is an RDP Server and the RDP
            Client option is set to User Selectable.
            - GUAC: Session is web-native.
            - RDP_CLIENT: User connects using an RDP client.
        server_id: str, optional
            Only applicable for sessions using non-container-based Server Pools.
            Specifies the exact server in the pool to use for the session.
        """
        payload = {k: v for k, v in locals().items() if v is not None and k not in ("self", "raise_on_error")}
        return await self.client.post("request-session", json=payload, raise_on_error=raise_on_error)

    async def status(
        self, user_id: str, session_id: str, skip_agent_check: bool = False, raise_on_error: bool = True
    ) -> ClientResponse:
        """Retrieve the status of an existing session.

        This call also updates the session token for the user, creating a new
        connection link and invalidating the old one.

        You should wait until the sessions reaches a `running` operational
        status before directing the end user into the session.

        If the session is not in a `running` state, the `kasm` object may not be
        provided, in which case the caller should interrogate the top level
        `operational_status`. `operational_progress` and `operational_message`
        may be used to provide context to the user.

        Use `skip_agent_check` to skip connecting out to the agent to verify
        status of the container, instead use the current value in the database
        for the status.

        Permission Required: `Users Auth Session` and `User`.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#get-kasm-status
        """
        payload = {"user_id": user_id, "kasm_id": session_id, "skip_agent_check": skip_agent_check}
        return await self.client.post("status-session", json=payload, raise_on_error=raise_on_error)

    async def join(self, user_id: str, shared_id: str, raise_on_error: bool = True) -> ClientResponse:
        """Join an existing session.

        Return the status of the shared Kasm and a join url to connect to the
        session as a view-only user.

        Permission Required: `Users Auth Session` and `User`.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#join-kasm
        """
        payload = {"user_id": user_id, "shared_id": shared_id}
        return await self.client.post("join-session", json=payload, raise_on_error=raise_on_error)

    async def get(self, raise_on_error: bool = True) -> ClientResponse:
        """Retrieve a list of live sessions.

        Use `status` if you want to retrieve information about a specific
        session.

        Permission Required: `Sessions View`

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#get-kasms
        """
        return await self.client.post("get-sessions", raise_on_error=raise_on_error)

    async def destroy(
        self, user_id: str, session_id: str, raise_on_error: bool = True, **kwargs: Any
    ) -> ClientResponse:
        """Destroy a Kasm session.

        The backend system my destroy the session immediately or queue the task
        for further processing prior to deletion such as saving off persistent
        profiles.
        If integrators wish to confirm the session is fully deleted, follow-up
        calls to `status()` may be called. An error will be thrown to confirm
        the session no longer exists.

        Permission Required: `Users Auth Session` and `User`.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#destroy-kasm
        """
        payload = {"user_id": user_id, "kasm_id": session_id}
        return await self.client.post("destroy-session", json=payload, raise_on_error=raise_on_error)

    async def keepalive(self, session_id: str, raise_on_error: bool = True) -> ClientResponse:
        """Issue a keepalive to reset the expiration time of a Kasm session.

        The new expiration time will be updated to reflect the
        `keepalive_expiration` Group Setting assigned to the Kasm's associated
        user.

        Permission Required: `Users Auth Session` and `User`.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#keepalive
        """
        payload = {"kasm_id": session_id}
        return await self.client.post("keepalive-session", json=payload, raise_on_error=raise_on_error)

    async def execute(
        self,
        user_id: str,
        session_id: str,
        command: str,
        workdir: str,
        environment: dict[str, str] = None,
        privileged: bool = False,
        user: str = None,
        raise_on_error: bool = True,
    ) -> ClientResponse:
        """Execute an arbitrary command inside a user's session.

        Parameters
        ----------
        user_id: str
            The ID of the user to whom the session belongs.
        session_id: str
            The ID of the Kasm session for the command will be executed on.
        command: str
            The command to execute inside the user's container.
        workdir: str
            The working directory path for the exec session inside the container.
        environment: dict[str, str], optional
            Environment variables to set for the exec session.
        privileged: bool, optional
            If `True`, runs the exec session with privileged permissions.
            Default to `False`.
        user: str, optional
            The user to run the command as. By default, the session runs as the
            sandboxed user. Set to "root" to run as root, which disables sandbox
            protections. Any value other than "root" may cause the command to
            fail.
        """
        payload = {
            "user_id": user_id,
            "kasm_id": session_id,
            "exec_config": {
                "cmd": command,
                "workdir": workdir,
                "privileged": privileged,
            },
        }
        if environment is not None:
            payload["exec_config"]["environment"] = environment
        if user is not None:
            payload["exec_config"]["user"] = user
        return await self.client.post("execute-session", json=payload, raise_on_error=raise_on_error)
