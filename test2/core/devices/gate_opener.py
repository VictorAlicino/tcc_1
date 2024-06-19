"""Generic Class for Gate Openers"""

from uuid import UUID
from enum import Enum
from abc import abstractmethod
from .__generic import OpusDevice, DeviceType

class GateOpener(OpusDevice):
    def __init__(self, name: str,
                 uuid: UUID,
                 driver: any):
        super().__init__()
        self.name = name
        self.id = uuid
        self.driver = driver

        self.building_id = None
        self.space_id = None
        self.room_id = None

        self.type = DeviceType.GATE_OPENER

        self.lock_state: bool  # Is the door locked or unlocked
        self.battery_level: float | None
        self.is_open: bool | None

    @abstractmethod
    def open(self) -> None:
        """Open the gate"""

    @abstractmethod
    def close(self) -> None:
        """Close the gate"""

    @abstractmethod
    def get_battery_level(self) -> float:
        """Get the battery level"""

    @abstractmethod
    def is_open(self) -> bool:
        """Check if the gate is open"""
