"""Generic Class for HVAC Units"""

from uuid import UUID
from enum import Enum
from abc import abstractmethod
from .__generic import OpusDevice, DeviceType

class HVACLevels(Enum):
    """Enum for HVAC Levels"""
    AUTO = 0
    LOW = 1
    MIN = 2
    MEDIUM = 3
    HIGH = 4
    MAX = 5

type hvac_levels_t = HVACLevels

class OpusHVAC(OpusDevice):
    """Generic Implementation of a hVAC Unit"""
    def __init__(self, name: str,
                 uuid: UUID,
                 driver: any):
        super().__init__()
        self.name = name
        self.id = uuid
        self.driver = driver
        self.type = DeviceType.HVAC

        self.power_state: str  # Is the light On or Off
        self.vendor: str | None
        self.model: str | None
        self.mode: str | None
        self.fan_speed: hvac_levels_t | None
        self.swing_vertical: hvac_levels_t | None
        self.swing_horizontal: str | None
        self.is_celsius: bool | None
        self.temperature: float
        # Dubious values
        self.quiet: bool | None
        self.turbo: bool | None
        self.economy: bool | None
        self.light: bool | None
        self.filter: bool | None
        self.clean: bool | None
        self.beep: bool | None
        self.sleep: int | None
        self.state_mode: str | None

    @abstractmethod
    def on(self) -> None:
        """Turn the HVAC on"""

    @abstractmethod
    def off(self) -> None:
        """Turn the HVAC off"""

    @abstractmethod
    def get_state(self) -> bool:
        """Get the state of the HVAC"""
        return {
            "power_state": self.power_state,
            "vendor": self.vendor,
            "model": self.model,
            "mode": self.mode,
            "fan_speed": self.fan_speed,
            "swing_vertical": self.swing_vertical,
            "swing_horizontal": self.swing_horizontal,
            "is_celsius": self.is_celsius,
            "temperature": self.temperature,
            "quiet": self.quiet,
            "turbo": self.turbo,
            "economy": self.economy,
            "light": self.light,
            "filter": self.filter,
            "clean": self.clean,
            "beep": self.beep,
            "sleep": self.sleep,
            "state_mode": self.state_mode
        }
