"""Generic Device Class"""
from uuid import UUID

class DeviceType(enumerate):
    """Enumerate for Device Types"""
    UNKNOWN = "UNKNOWN"
    LIGHT = "LIGHT"
    HVAC = "HVAC"
    PROJECTOR = "PROJECTOR"
    GATE_OPENER = "GATE_OPENER"
    DOOR_LOCK = "DOOR_LOCK"


class OpusDevice():
    """Generic Device Class"""
    def __init__(self):
        self.name: str
        self.id: UUID | None
        self.room_id: UUID | None
        self.space_id: UUID | None
        self.building_id: UUID | None
        self.driver: any
        self.type: DeviceType
