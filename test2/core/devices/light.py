"""Generic Class for Light"""
from abc import abstractmethod
from .__generic import OpusDevice, DeviceType

class OpusHSL(enumerate):
    H: float    #  Hue
    S: float    # Saturation
    L: float    # Lightness    

class OpusLight(OpusDevice):
    """Generic Implementation of a Light"""
    def __init__(self, name: str,
                 uuid: str,
                 driver: any):
        super().__init__()
        self.name = name
        self.id = uuid
        self.room_id = None
        self.space_id = None
        self.building_id = None
        self.driver = driver
        self.type = DeviceType.LIGHT
        self.power_state: bool  # Is the HVAC On or Off
        self.hsl_color: OpusHSL  # Hue, Saturation, Lightness

    @abstractmethod
    def on(self) -> None:
        """Turn the light on"""

    @abstractmethod
    def off(self) -> None:
        """Turn the light off"""

    @abstractmethod
    def get_state(self) -> bool:
        """Get the state of the light"""
        return {
            "power_state": self.power_state
        }
