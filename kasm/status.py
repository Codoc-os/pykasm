class Status:
    """Represent a Kasm session status."""

    STARTING = "starting"
    RUNNING = "running"

    def __init__(self, value: str, progress: int = None, message: str = None) -> None:
        self.value = value
        self.progress = progress
        self.message = message

    def __hash__(self) -> int:
        return hash(self.value)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.value == other.value
        if isinstance(other, str):
            return self.value == other
        return NotImplemented

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value}, {self.progress}, {self.message})"

    def __str__(self) -> str:
        return self.value
