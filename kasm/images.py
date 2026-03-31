from typing import Any, Self

from kasm.abc import KasmObject
from kasm.connections import async_connections, connections
from kasm.enums import CpuAllocationMethod


class ImageAttribute:
    """Represent a Kasm image attribute."""

    def __init__(self, attr_id: str, image: "Image", name: str, category: str, value: str) -> None:
        self.attr_id = attr_id
        self.image = image
        self.name = name
        self.category = category
        self.value = value


class Image(KasmObject):
    """Represent a Kasm image."""

    def __init__(
        self,
        using: str | None,
        image_id: str,
        name: str | None = None,
        friendly_name: str | None = None,
        description: str | None = None,
        image_type: str | None = None,
        image_src: str | None = None,
        hash: str | None = None,
        docker_registry: str | None = None,
        docker_user: str | None = None,
        docker_token: str | None = None,
        uncompressed_size_mb: int | None = None,
        x_res: int | None = None,
        y_res: int | None = None,
        hidden: bool | None = None,
        memory: int | None = None,
        cores: float | None = None,
        cpu_allocation_method: CpuAllocationMethod | None = None,
        require_gpu: bool | None = None,
        gpu_count: int | None = None,
        zone_id: str | None = None,
        zone_name: str | None = None,
        restrict_to_zone: bool | None = None,
        server_id: str | None = None,
        restrict_to_server: bool | None = None,
        server_pool_id: str | None = None,
        restrict_to_network: bool | None = None,
        restrict_network_names: list[str] | None = None,
        allow_network_selection: bool | None = None,
        override_egress_gateways: bool | None = None,
        enabled: bool | None = None,
        available: bool | None = None,
        session_time_limit: str | None = None,
        session_banner: str | None = None,
        session_banner_id: str | None = None,
        session_banner_force_disabled: bool | None = None,
        persistent_profile_path: str | None = None,
        persistent_profile_config: dict[str, str] | None = None,
        enforce_workspace_persistence: bool | None = None,
        is_remote_app: bool | None = None,
        remote_app_name: str | None = None,
        remote_app_args: str | None = None,
        remote_app_icon: str | None = None,
        remote_app_program: str | None = None,
        link_url: str | None = None,
        categories: list[str] | None = None,
        default_category: str | None = None,
        include_labels: list[str] | None = None,
        exclude_labels: list[str] | None = None,
        filter_policy_id: str | None = None,
        filter_policy_name: str | None = None,
        filter_policy_force_disabled: bool | None = None,
        image_attributes: list[ImageAttribute] | None = None,
        notes: str | None = None,
        volume_mappings: dict[str, Any] | None = None,
        launch_config: dict[str, Any] | None = None,
        run_config: dict[str, Any] | None = None,
        exec_config: dict[str, Any] | None = None,
        server: dict[str, Any] | None = None,
        server_pool: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(using)
        self.image_id = self._normalize_id(image_id)
        self.name = name
        self.friendly_name = friendly_name
        self.description = description
        self.image_type = image_type
        self.image_src = image_src
        self.hash = hash
        self.docker_registry = docker_registry
        self.docker_user = docker_user
        self.docker_token = docker_token
        self.uncompressed_size_mb = uncompressed_size_mb
        self.x_res = x_res
        self.y_res = y_res
        self.hidden = hidden
        self.memory = memory
        self.cores = cores
        self.cpu_allocation_method = cpu_allocation_method
        self.require_gpu = require_gpu
        self.gpu_count = gpu_count
        self.zone_id = zone_id
        self.zone_name = zone_name
        self.restrict_to_zone = restrict_to_zone
        self.server_id = server_id
        self.restrict_to_server = restrict_to_server
        self.server_pool_id = server_pool_id
        self.restrict_to_network = restrict_to_network
        self.restrict_network_names = restrict_network_names or []
        self.allow_network_selection = allow_network_selection
        self.override_egress_gateways = override_egress_gateways
        self.enabled = enabled
        self.available = available
        self.session_time_limit = session_time_limit
        self.session_banner = session_banner
        self.session_banner_id = session_banner_id
        self.session_banner_force_disabled = session_banner_force_disabled
        self.persistent_profile_path = persistent_profile_path
        self.persistent_profile_config = persistent_profile_config or {}
        self.enforce_workspace_persistence = enforce_workspace_persistence
        self.is_remote_app = is_remote_app
        self.remote_app_name = remote_app_name
        self.remote_app_args = remote_app_args
        self.remote_app_icon = remote_app_icon
        self.remote_app_program = remote_app_program
        self.link_url = link_url
        self.categories = categories or []
        self.default_category = default_category
        self.include_labels = include_labels or []
        self.exclude_labels = exclude_labels or []
        self.filter_policy_id = filter_policy_id
        self.filter_policy_name = filter_policy_name
        self.filter_policy_force_disabled = filter_policy_force_disabled
        self.image_attributes = image_attributes or []
        self.notes = notes
        self.volume_mappings = volume_mappings or {}
        self.launch_config = launch_config or {}
        self.run_config = run_config or {}
        self.exec_config = exec_config or {}
        self.server = server or {}
        self.server_pool = server_pool or {}

    def __repr__(self) -> str:
        return f"<Image: {self.image_id} - {self.friendly_name}>"

    @classmethod
    def _from_response(cls, using: str | None, data: dict[str, Any]) -> Self:
        """Create an instance from the typical API response structure.

        `data` must be the dictionary containing the instance information, e.g.
            * `{ "image_id": "<id>", ...}`
        not
            * `{ "image": { "image_id": "<id>", ...}}`.
        """
        image = cls(
            using=using,
            image_id=data["image_id"],
            name=data["name"],
            friendly_name=data.get("friendly_name"),
            description=data.get("description"),
            image_type=data.get("image_type"),
            image_src=data.get("image_src"),
            hash=data.get("hash"),
            docker_registry=data.get("docker_registry"),
            docker_user=data.get("docker_user"),
            docker_token=data.get("docker_token"),
            uncompressed_size_mb=data.get("uncompressed_size_mb"),
            x_res=data.get("x_res"),
            y_res=data.get("y_res"),
            hidden=data.get("hidden"),
            memory=data.get("memory"),
            cores=data.get("cores"),
            cpu_allocation_method=data.get("cpu_allocation_method"),
            require_gpu=data.get("require_gpu"),
            gpu_count=data.get("gpu_count"),
            zone_id=data.get("zone_id"),
            zone_name=data.get("zone_name"),
            restrict_to_zone=data.get("restrict_to_zone"),
            server_id=data.get("server_id"),
            restrict_to_server=data.get("restrict_to_server"),
            server_pool_id=data.get("server_pool_id"),
            restrict_to_network=data.get("restrict_to_network"),
            restrict_network_names=data.get("restrict_network_names"),
            allow_network_selection=data.get("allow_network_selection"),
            override_egress_gateways=data.get("override_egress_gateways"),
            enabled=data.get("enabled"),
            available=data.get("available"),
            session_time_limit=data.get("session_time_limit"),
            session_banner=data.get("session_banner"),
            session_banner_id=data.get("session_banner_id"),
            session_banner_force_disabled=data.get("session_banner_force_disabled"),
            persistent_profile_path=data.get("persistent_profile_path"),
            persistent_profile_config=data.get("persistent_profile_config"),
            enforce_workspace_persistence=data.get("enforce_workspace_persistence"),
            is_remote_app=data.get("is_remote_app"),
            remote_app_name=data.get("remote_app_name"),
            remote_app_args=data.get("remote_app_args"),
            remote_app_icon=data.get("remote_app_icon"),
            remote_app_program=data.get("remote_app_program"),
            link_url=data.get("link_url"),
            categories=data.get("categories"),
            default_category=data.get("default_category"),
            include_labels=data.get("include_labels"),
            exclude_labels=data.get("exclude_labels"),
            filter_policy_id=data.get("filter_policy_id"),
            filter_policy_name=data.get("filter_policy_name"),
            filter_policy_force_disabled=data.get("filter_policy_force_disabled"),
            notes=data.get("notes"),
            volume_mappings=data.get("volume_mappings"),
            launch_config=data.get("launch_config"),
            run_config=data.get("run_config"),
            exec_config=data.get("exec_config"),
            server=data.get("server"),
            server_pool=data.get("server_pool"),
        )
        image.image_attributes = [
            ImageAttribute(attr_id=a["attr_id"], image=image, name=a["name"], category=a["category"], value=a["value"])
            for a in data.get("imageAttributes", [])
        ]
        return image

    @classmethod
    def all(cls, using: str | None = None) -> list[Self]:
        """Retrieve a list of available images.

        Permission Required: `Images View`

        For more information, see:
        https://docs.kasm.com/docs/latest/developers/developer_api/index.html#get-images
        """
        data = connections.get_connection(using).images.get().json()
        return [cls._from_response(using, image) for image in data["images"]]

    @classmethod
    async def aall(cls, using: str | None = None) -> list[Self]:
        """Retrieve a list of available images.

        Permission Required: `Images View`

        For more information, see:
        https://docs.kasm.com/docs/latest/developers/developer_api/index.html#get-images
        """
        data = (await async_connections.get_connection(using).images.get()).json()
        return [cls._from_response(using, image) for image in data["images"]]

    @classmethod
    def get(cls, image_id: str, using: str | None = None) -> Self | None:
        """Retrieve a list of available images.

        Permission Required: `Images View`.

        For more information, see:
        https://docs.kasm.com/docs/latest/developers/developer_api/index.html#get-images
        """
        return next((image for image in cls.all(using=using) if image.image_id == image_id), None)

    @classmethod
    async def aget(cls, image_id: str, using: str | None = None) -> Self | None:
        """Retrieve a list of available images.

        Permission Required: `Images View`.

        For more information, see:
        https://docs.kasm.com/docs/latest/developers/developer_api/index.html#get-images
        """
        return next((image for image in await cls.aall(using=using) if image.image_id == image_id), None)

    def refresh(self) -> Self | None:
        """Refresh the instance data from the API."""
        return self.get(self.image_id)

    async def arefresh(self) -> Self | None:
        """Refresh the instance data from the API."""
        return await self.aget(self.image_id)
