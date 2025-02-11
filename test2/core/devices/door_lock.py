"""Generic Class for Door Locks"""

from uuid import UUID
from enum import Enum
from abc import abstractmethod
from .__generic import OpusDevice, DeviceType

class DoorLock(OpusDevice):
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

        self.type = DeviceType.DOOR_LOCK

        self.lock_state: bool  # Is the door locked or unlocked
        self.battery_level: float | None
        self.is_open: bool | None

    @abstractmethod
    def lock(self) -> None:
        """Lock the door"""

    @abstractmethod
    def unlock(self) -> None:
        """Unlock the door"""

    @abstractmethod
    def get_battery_level(self) -> float:
        """Get the battery level"""

    @abstractmethod
    def is_open(self) -> bool:
        """Check if the door is open"""

    @abstractmethod
    def get_state(self) -> bool:
        """Get the state of the door lock"""
        return {
            "lock_state": self.lock_state
        }
