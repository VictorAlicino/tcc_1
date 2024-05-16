"""Generic Class for Light"""
from abc import abstractmethod
from .__generic import OpusDevice

class OpusLight(OpusDevice):
    """Generic Implementation of a Light"""
    def __init__(self, name: str,
                 uuid: str,
                 room_id: str,
                 space_id: str,
                 building: str,
                 driver: any):
        super().__init__()
        self.name = name
        self.id = uuid
        self.room_id = room_id
        self.space_id = space_id
        self.building = building
        self.driver = driver
        self.power_state: bool  # Is the HVAC On or Off

    @abstractmethod
    async def on(self) -> None:
        """Turn the light on"""

    @abstractmethod
    async def off(self) -> None:
        """Turn the light off"""
