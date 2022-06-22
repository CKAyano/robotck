from enum import Enum, auto


class DHAngleType(Enum):
    RAD = auto()
    DEG = auto()


class DHType(Enum):
    STANDARD = auto()
    MODIFIED = auto()
