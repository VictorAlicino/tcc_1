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
            "power_state": getattr(self, "power_state", None) or None,
            "vendor": getattr(self, "vendor", None) or None,
            "model": getattr(self, "model", None) or None,
            "mode": getattr(self, "mode", None) or None,
            "fan_speed": getattr(self, "fan_speed", None) or None,
            "swing_vertical": getattr(self, "swing_vertical", None) or None,
            "swing_horizontal": getattr(self, "swing_horizontal", None) or None,
            "is_celsius": getattr(self, "is_celsius", None) or None,
            "temperature": getattr(self, "temperature", None) or None,
            "quiet": getattr(self, "quiet", None) or None,
            "turbo": getattr(self, "turbo", None) or None,
            "economy": getattr(self, "economy", None) or None,
            "light": getattr(self, "light", None) or None,
            "filter": getattr(self, "filter", None) or None,
            "clean": getattr(self, "clean", None) or None,
            "beep": getattr(self, "beep", None) or None,
            "sleep": getattr(self, "sleep", None) or None,
            "state_mode": getattr(self, "state_mode", None) or None,
        }
    
    @abstractmethod
    def set_state(self, state: dict) -> None:
        """Set the state of the HVAC"""
        self.power_state = state.get("power_state", None)
        self.vendor = state.get("vendor", None)
        self.model = state.get("model", None)
        self.mode = state.get("mode", None)
        self.fan_speed = state.get("fan_speed", None)
        self.swing_vertical = state.get("swing_vertical", None)
        self.swing_horizontal = state.get("swing_horizontal", None)
        self.is_celsius = state.get("is_celsius", None)
        self.temperature = state.get("temperature", None)
        self.quiet = state.get("quiet", None)
        self.turbo = state.get("turbo", None)
        self.economy = state.get("economy", None)
        self.light = state.get("light", None)
        self.filter = state.get("filter", None)
        self.clean = state.get("clean", None)
        self.beep = state.get("beep", None)
        self.sleep = state.get("sleep", None)
        self.state_mode = state.get("state_mode", None)
