import datetime
from typing import Any, Self
from urllib.parse import urlencode, urljoin

from kasm.abc import KasmObject
from kasm.connections import async_connections, connections
from kasm.enums import PersistentProfileMode, RdpClientType
from kasm.images import Image
from kasm.status import Status
from kasm.users import User


class Session(KasmObject):
    """Represent a Kasm session.

    Attributes other than `session_id`, `user` and `status` should not be relied
    upon as long as `status` is not equal to `Status.RUNNING`.
    """

    def __init__(
        self,
        using: str | None,
        session_id: str,
        user: User,
        status: Status | None = None,
        image: Image | None = None,
        url: str | None = None,
        host: str | None = None,
        port: int | None = None,
        token: str | None = None,
        view_only_token: str | None = None,
        share_id: str | None = None,
        container_id: str | None = None,
        container_ip: str | None = None,
        docker_network: str | None = None,
        server_id: str | None = None,
        zone_name: str | None = None,
        hostname: str | None = None,
        point_of_presence: str | None = None,
        cores: float | None = None,
        memory: int | None = None,
        gpus: int | None = None,
        start_date: datetime.datetime | None = None,
        expiration_date: datetime.datetime | None = None,
        keepalive_date: datetime.datetime | None = None,
        created_date: datetime.datetime | None = None,
        is_persistent_profile: bool | None = None,
        persistent_profile_mode: PersistentProfileMode | None = None,
        client_settings: dict[str, str | int | bool] | None = None,
        port_map: dict[str, dict[str, str | int]] | None = None,
        connection_info: dict[str, str] | None = None,
        egress_gateway_id: str | None = None,
        egress_credential_id: str | None = None,
        egress_provider_name: str | None = None,
        egress_gateway_name: str | None = None,
        egress_gateway_country: str | None = None,
        egress_gateway_city: str | None = None,
        rdp_client_type: str | None = None,
        is_standby: bool | None = None,
        agent_installed: bool | None = None,
        operational_message: str | None = None,
        operational_progress: int | None = None,
        autoscale_config_id: str | None = None,
        staging_config_id: str | None = None,
        cast_config_id: str | None = None,
        connection_proxy_id: str | None = None,
        connection_credential: str | None = None,
        border: str | None = None,
        queued_tasks: list | None = None,
    ) -> None:
        super().__init__(using=using)
        self.session_id = self._normalize_id(session_id)
        self.user = user
        self.status = status
        self.image = image
        self._url = url
        self.host = host
        self.port = port
        self.token = token
        self.view_only_token = view_only_token
        self.share_id = share_id
        self.container_id = container_id
        self.container_ip = container_ip
        self.docker_network = docker_network
        self.server_id = server_id
        self.zone_name = zone_name
        self.hostname = hostname
        self.point_of_presence = point_of_presence
        self.cores = cores
        self.memory = memory
        self.gpus = gpus
        self.start_date = start_date
        self.expiration_date = expiration_date
        self.keepalive_date = keepalive_date
        self.created_date = created_date
        self.is_persistent_profile = is_persistent_profile
        self.persistent_profile_mode = persistent_profile_mode
        self.client_settings = client_settings or {}
        self.port_map = port_map or {}
        self.connection_info = connection_info or {}
        self.egress_gateway_id = egress_gateway_id
        self.egress_credential_id = egress_credential_id
        self.egress_provider_name = egress_provider_name
        self.egress_gateway_name = egress_gateway_name
        self.egress_gateway_country = egress_gateway_country
        self.egress_gateway_city = egress_gateway_city
        self.rdp_client_type = rdp_client_type
        self.is_standby = is_standby
        self.agent_installed = agent_installed
        self.operational_message = operational_message
        self.operational_progress = operational_progress
        self.autoscale_config_id = autoscale_config_id
        self.staging_config_id = staging_config_id
        self.cast_config_id = cast_config_id
        self.connection_proxy_id = connection_proxy_id
        self.connection_credential = connection_credential
        self.border = border
        self.queued_tasks = queued_tasks or []

    def __repr__(self) -> str:
        return f"<Session {self.session_id} - {self.user!r}>"

    def url(
        self,
        disable_control_panel: bool = False,
        disable_tips: bool = False,
        disable_viewers: bool = False,
        disable_fix_res: bool = False,
        using: str | None = None,
    ) -> str | None:
        """Return the URL of the session.

        If the session was retrieve with `Session.all()`, no URL will be
        provided, use `refresh()` to retrieve a session with an URL.

        Parameters
        ----------
        disable_control_panel : bool, optional
            If set to `True`, hides the Kasm control panel normally used for
            uploads, downloads etc. Users will be unable to access this
            functionality.
        disable_tips : bool, optional
            If set to `True`, stops the tips modal from showing when the user
            connects to a session.
        disable_viewers : bool, optional
            If set to `True`, hides the list of viewers for shared sessions.
        disable_fix_res : bool, optional
            By default, shared sessions are forced into a fixed resolution
            and aspect ratio. Setting this argument to `True` will allow the
            shared session to operate with a dynamic resolution and aspect
            ratio.
        using : str | None, optional
            The using parameter, by default None
        """
        if self._url is None:
            return None

        base_url = urljoin(self.client(using).url, self._url)
        params = {
            "disable_control_panel": int(disable_control_panel),
            "disable_tips": int(disable_tips),
            "disable_viewers": int(disable_viewers),
            "disable_fix_res": int(disable_fix_res),
        }
        params = {k: v for k, v in params.items() if v}
        if not params:
            return base_url
        return f"{base_url}?{urlencode(params)}"

    @classmethod
    def _from_response_starting(cls, using: str | None, user: User, data: dict[str, Any]) -> Self:
        """Create an instance from the typical API response structure from a non-running session."""
        return cls(
            using=using,
            session_id=data["kasm_id"],
            status=Status(data["status"]),
            user=user,
        )

    @classmethod
    def _from_response_running(cls, using: str | None, user: User, image: Image | None, data: dict[str, Any]) -> Self:
        """Create an instance from the typical API response structure from a running session.

        `data` must be the dictionary containing the instance information, e.g.
            * `{ "kasm_id": "<id>", ...}`
        not
            * `{ "kasm": { "kasm_id": "<id>", ...}}`.
        """
        if data.get("start_date") == "None":
            data["start_date"] = None
        if data.get("expiration_date") == "None":
            data["expiration_date"] = None
        if data.get("keepalive_date") == "None":
            data["keepalive_date"] = None
        if data.get("created_date") == "None":
            data["created_date"] = None
        return cls(
            using=using,
            session_id=data["kasm_id"],
            user=user,
            status=Status(data["operational_status"]),
            image=image,
            url=data.get("url"),
            host=data.get("host"),
            port=data.get("port"),
            token=data.get("token"),
            view_only_token=data.get("view_only_token"),
            share_id=data.get("share_id"),
            container_id=data.get("container_id"),
            container_ip=data.get("container_ip"),
            docker_network=data.get("docker_network"),
            server_id=data.get("server_id"),
            zone_name=data.get("zone_name"),
            hostname=data.get("hostname"),
            point_of_presence=data.get("point_of_presence"),
            cores=data.get("cores"),
            memory=data.get("memory"),
            gpus=data.get("gpus"),
            start_date=data.get("start_date") and datetime.datetime.fromisoformat(data["start_date"]),
            expiration_date=data.get("expiration_date") and datetime.datetime.fromisoformat(data["expiration_date"]),
            keepalive_date=data.get("keepalive_date") and datetime.datetime.fromisoformat(data["keepalive_date"]),
            created_date=data.get("created_date") and datetime.datetime.fromisoformat(data["created_date"]),
            is_persistent_profile=data.get("is_persistent_profile"),
            persistent_profile_mode=data.get("persistent_profile_mode"),
            client_settings=data.get("client_settings"),
            port_map=data.get("port_map"),
            connection_info=data.get("connection_info"),
            egress_gateway_id=data.get("egress_gateway_id"),
            egress_credential_id=data.get("egress_credential_id"),
            egress_provider_name=data.get("egress_provider_name"),
            egress_gateway_name=data.get("egress_gateway_name"),
            egress_gateway_country=data.get("egress_gateway_country"),
            egress_gateway_city=data.get("egress_gateway_city"),
            rdp_client_type=data.get("rdp_client_type"),
            is_standby=data.get("is_standby"),
            agent_installed=data.get("agent_installed"),
            operational_message=data.get("operational_message"),
            operational_progress=data.get("operational_progress"),
            autoscale_config_id=data.get("autoscale_config_id"),
            staging_config_id=data.get("staging_config_id"),
            cast_config_id=data.get("cast_config_id"),
            connection_proxy_id=data.get("connection_proxy_id"),
            connection_credential=data.get("connection_credential"),
            border=data.get("border"),
            queued_tasks=data.get("queued_tasks"),
        )

    @classmethod
    def all(cls, using: str | None = None) -> list[Self]:
        """Retrieve a list of running sessions.

        You can request a specific session by providing

        Permission Required: `Sessions View`

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#get-kasms
        """
        data = connections.get_connection(using).sessions.get().json()
        sessions = []
        users = {u.user_id: u for u in User.all(using=using)}
        images = {i.image_id: i for i in Image.all(using=using)}
        for session in data["kasms"]:
            user_id = cls._normalize_id(session["user_id"])
            image_id = cls._normalize_id(session["image_id"])
            sessions.append(cls._from_response_running(using, users[user_id], images[image_id], session))
        return sessions

    @classmethod
    async def aall(cls, using: str | None = None) -> list[Self]:
        """Retrieve a list of running sessions.

        You can request a specific session by providing

        Permission Required: `Sessions View`

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#get-kasms
        """
        data = (await async_connections.get_connection(using).sessions.get()).json()
        sessions = []
        users = {u.user_id: u for u in await User.aall(using=using)}
        images = {i.image_id: i for i in await Image.aall(using=using)}
        for session in data["kasms"]:
            user_id = cls._normalize_id(session["user_id"])
            image_id = cls._normalize_id(session["image_id"])
            sessions.append(cls._from_response_running(using, users[user_id], images[image_id], session))
        return sessions

    @classmethod
    def get(cls, session_id: str, user: str | User, using: str | None = None) -> Self:
        """Retrieve a specific session.

        Permission Required: `Users Auth Session` and `User`.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#get-kasm-status
        """
        if isinstance(user, str):
            user = User.get(user_id=user, using=using)
        session = cls(using=using, session_id=session_id, user=user)
        return session.update_status(using=using)

    @classmethod
    async def aget(cls, session_id: str, user: str | User, using: str | None = None) -> Self:
        """Retrieve a specific session.

        Permission Required: `Users Auth Session` and `User`.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#get-kasm-status
        """
        if isinstance(user, str):
            user = await User.aget(user_id=user, using=using)
        session = cls(using=using, session_id=session_id, user=user)
        return await session.aupdate_status(using=using)

    @classmethod
    def request(
        cls,
        user: User | str,
        image: Image | str,
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
        using: str | None = None,
    ) -> Self:
        """Request a new session to be created.

        Use `update_status()` to ensure the session reaches a running state,
        before directing the user to the session.

        Permission Required: `Users Auth Session` and `User`.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#request-kasm

        Parameters
        ----------
        user: User | str
            If specified, the Kasm session will be created under this user. The
            value must be an instance of `User` or the `user_id` string.
        image: Image | str
            The ID of the image to use for the Kasm session. The value
            must be an instance of `Image` or the `image_id` string.
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
        user_instance: User = User.get(user_id=user, using=using) if isinstance(user, str) else user
        data = (
            connections.get_connection(using)
            .sessions.request(
                user_instance.user_id,
                image if isinstance(image, str) else image.image_id,
                enable_sharing,
                kasm_url,
                environment,
                connection_info,
                client_language,
                client_timezone,
                egress_gateway_id,
                persistent_profile_mode,
                rdp_client_type,
                server_id,
            )
            .json()
        )
        return cls._from_response_starting(using, user_instance, data)

    @classmethod
    async def arequest(
        cls,
        user: User | str,
        image: Image | str,
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
        using: str | None = None,
    ) -> Self:
        """Request a new session to be created.

        Use `update_status()` to ensure the session reaches a running state,
        before directing the user to the session.

        Permission Required: `Users Auth Session` and `User`.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#request-kasm

        Parameters
        ----------
        user: User | str
            If specified, the Kasm session will be created under this user. The
            value must be an instance of `User` or the `user_id` string.
        image: Image | str
            The ID of the image to use for the Kasm session. The value
            must be an instance of `Image` or the `image_id` string.
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
        user_instance: User = (await User.aget(user_id=user, using=using)) if isinstance(user, str) else user
        data = (
            await async_connections.get_connection(using).sessions.request(
                user_instance.user_id,
                image if isinstance(image, str) else image.image_id,
                enable_sharing,
                kasm_url,
                environment,
                connection_info,
                client_language,
                client_timezone,
                egress_gateway_id,
                persistent_profile_mode,
                rdp_client_type,
                server_id,
            )
        ).json()
        return cls._from_response_starting(using, user_instance, data)

    def refresh(self) -> Self:
        """Refresh the instance data from the API."""
        return self.get(self.session_id, self.user)

    async def arefresh(self) -> Self:
        """Refresh the instance data from the API."""
        return await self.aget(self.session_id, self.user)

    def update_status(self, skip_agent_check: bool = False, using: str | None = None) -> Self:
        """Return an new instance with its status updated.

        This call updates the session token for the user, creating a new
        connection url and invalidating the old one.

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
        data = (
            self.client(using)
            .sessions.status(user_id=self.user.user_id, session_id=self.session_id, skip_agent_check=skip_agent_check)
            .json()
        )
        if "kasm" not in data:
            return self._from_response_starting(using, self.user, data)
        image = Image.get(data["kasm"]["image"]["image_id"], using=using) if data["kasm"].get("image") else None
        data["kasm"]["url"] = data["kasm_url"]
        return self._from_response_running(using, self.user, image, data["kasm"])

    async def aupdate_status(self, skip_agent_check: bool = False, using: str | None = None) -> Self:
        """Return an new instance with its status updated.

        This call also updates the session token for the user, creating a new
        connection url and invalidating the old one.

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
        data = (
            await self.async_client(using).sessions.status(
                user_id=self.user.user_id, session_id=self.session_id, skip_agent_check=skip_agent_check
            )
        ).json()
        if "kasm" not in data:
            return self._from_response_starting(using, self.user, data)
        image = (
            (await Image.aget(data["kasm"]["image"]["image_id"], using=using)) if data["kasm"].get("image") else None
        )
        data["kasm"]["url"] = data["kasm_url"]
        return self._from_response_running(using, self.user, image, data["kasm"])

    def join(self, user: User | str, using: str | None = None) -> str | None:
        """Return the join url to connect to the session as a view-only user.

        Permission Required: `Users Auth Session` and `User`.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#join-kasm
        """
        if self.share_id is None:
            return None
        user_id = user.user_id if isinstance(user, User) else user
        data = self.client(using=using).sessions.join(user_id=user_id, shared_id=self.share_id).json()
        return urljoin(self.client(using=using).url, data["kasm_url"])

    async def ajoin(self, user: User | str, using: str | None = None) -> str | None:
        """Return the join url to connect to the session as a view-only user.

        Permission Required: `Users Auth Session` and `User`.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#join-kasm
        """
        if self.share_id is None:
            return None
        user_id = user.user_id if isinstance(user, User) else user
        data = (await self.async_client(using=using).sessions.join(user_id=user_id, shared_id=self.share_id)).json()
        return urljoin(self.async_client(using=using).url, data["kasm_url"])

    def destroy(self, using: str | None = None) -> Self:
        """Destroy the Kasm session.

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
        self.client(using=using).sessions.destroy(user_id=self.user.user_id, session_id=self.session_id)
        return self

    async def adestroy(self, using: str | None = None) -> Self:
        """Destroy the Kasm session.

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
        await self.async_client(using=using).sessions.destroy(user_id=self.user.user_id, session_id=self.session_id)
        return self

    def keepalive(self, using: str | None = None) -> Self:
        """Return a new instance with the updated expiration time.

        The new expiration time will be updated to reflect the
        `keepalive_expiration` Group Setting assigned to the Kasm's associated
        user.

        Permission Required: `Users Auth Session` and `User`.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#keepalive
        """
        self.client(using=using).sessions.keepalive(self.session_id)
        return self.update_status(using=using)

    async def akeepalive(self, using: str | None = None) -> Self:
        """Return a new instance with the updated expiration time.

        The new expiration time will be updated to reflect the
        `keepalive_expiration` Group Setting assigned to the Kasm's associated
        user.

        Permission Required: `Users Auth Session` and `User`.

        For more information, see:
        https://docs.kasm.com/docs/developers/developer_api#keepalive
        """
        await self.async_client(using=using).sessions.keepalive(self.session_id)
        return await self.aupdate_status(using=using)

    def execute(
        self,
        command: str,
        workdir: str,
        environment: dict[str, str] = None,
        privileged: bool = False,
        user: str = None,
        using: str | None = None,
    ) -> None:
        """Execute an arbitrary command inside a user's session.

        Parameters
        ----------
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
        self.client(using=using).sessions.execute(
            self.user.user_id, self.session_id, command, workdir, environment, privileged, user
        )

    async def aexecute(
        self,
        command: str,
        workdir: str,
        environment: dict[str, str] = None,
        privileged: bool = False,
        user: str = None,
        using: str | None = None,
    ) -> None:
        """Execute an arbitrary command inside a user's session.

        Parameters
        ----------
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
        await self.async_client(using=using).sessions.execute(
            self.user.user_id, self.session_id, command, workdir, environment, privileged, user
        )
