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

    def get(self):
        """Get the device"""
        return {
            "device_name": self.name,
            "device_pk": str(self.id),
            "device_type": self.type,
            "building_room_pk": str(self.room_id),
            "building_space_pk": str(self.space_id),
            "building_pk": str(self.building_id)
        }
