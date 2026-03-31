import enum


class PersistentProfileMode(str, enum.Enum):
    """Allowed values for the different modes for persistent profile management."""

    DISABLED = "Disabled"
    ENABLED = "Enabled"
    RESET = "Reset"


class RdpClientType(str, enum.Enum):
    """Allowed values for the different types of RDP clients."""

    GUAC = "GUAC"
    RDP_CLIENT = "RDP_CLIENT"


class CpuAllocationMethod(str, enum.Enum):
    """Allowed values for the different CPU allocation methods."""

    QUOTAS = "Quotas"
    SHARES = "Shares"
    INHERIT = "Inherit"
