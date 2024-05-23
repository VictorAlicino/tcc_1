"""Models for API endpoints."""
from pydantic import BaseModel

class Building(BaseModel):
    """Building model."""
    name: str

class Space(BaseModel):
    """Space model."""
    name: str
    building: str

class Room(BaseModel):
    """Room model."""
    name: str
    space: str
    building: str

class Device(BaseModel):
    """Device model."""
    id: str
    name: str
    driver: str
    room_id: str

# Driver specific models
class DeviceByDriver(BaseModel):
    """Device model."""
    device_type: str
    room_id: str
    device_name: str
    data: dict

# Commands

class Command(BaseModel):
    """Command model."""
    cmnd: str | dict
    set_temperature: float | None
    set_mode: str | dict | None
    set_fan_speed: str | dict | None

    