"""Generic Class for HVAC Units"""

from uuid import UUID
from enum import Enum

class HVACLevels(Enum):
    """Enum for HVAC Levels"""
    AUTO = 0
    LOW = 1
    MIN = 2
    MEDIUM = 3
    HIGH = 4
    MAX = 5

type hvac_levels_t = HVACLevels

class OpusHVAC():
    """Generic Implementation of a hVAC Unit"""
    def __init__(self):
        self.name: str
        self.id: UUID | None
        self.room_id: UUID | None
        self.space_id: UUID | None
        self.building: UUID | None

        self.power_state: bool  # Is the light On or Off
        self.vendor: str | None
        self.model: str | None
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

    async def on(self) -> None:
        """Turn the light on"""

    async def off(self) -> None:
        """Turn the light off"""
