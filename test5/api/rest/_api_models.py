"""Models for API endpoints."""
from pydantic import BaseModel, validator
from uuid import UUID

# Server Requests
class UserRole(BaseModel):
    """Role model."""
    user_id: str # User ID
    role: int

    @validator('user_id')
    def validate_uuid(cls, v):
        try:
            return str(UUID(v))  # Tenta converter a string para UUID
        except ValueError:
            raise ValueError('Invalid UUID format')
        
class VerifyToken(BaseModel):
    """Conductor Register Request"""
    access_token: str

class ConductorLogin(BaseModel):
    """Conductor Login Request"""
    email: str
    google_sub: str

class ConductorRegister(BaseModel):
    """Conductor Register Request"""
    email: str
    google_sub: str

class User(BaseModel):
    """User model."""
    user_id: UUID
    google_sub: str
    email: str
    name: str
    given_name: str
    family_name: str
    picture: str

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
