"""Models for API endpoints."""
from pydantic import BaseModel

# Server Requests
class Role(BaseModel):
    """Role model."""
    user_id: str
    server_id: str
    role: int

class ServerUserList(BaseModel):
    """Server User List model."""
    server_id: str
    users: list

class ConductorLogin(BaseModel):
    """Conductor Login Request"""
    email: str
    google_sub: str

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
    temperature: float | None
    mode: str | dict | None
    fan_speed: str | dict | None
