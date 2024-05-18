"""DB Schemas for Pydantic Models"""
from pydantic import BaseModel
from typing import List, Optional

# Building Schemas
class BuildingBase(BaseModel):
    building_name: str

class BuildingCreate(BuildingBase):
    pass

class Building(BuildingBase):
    building_pk: bytes

    class Config:
        orm_mode: True

# Building Space Schemas
class BuildingSpaceBase(BaseModel):
    space_name: str
    building_fk: bytes

class BuildingSpaceCreate(BuildingSpaceBase):
    pass

class BuildingSpace(BuildingSpaceBase):
    building_space_pk: bytes

    class Config:
        orm_mode: True

# Building Room Schemas
class BuildingRoomBase(BaseModel):
    room_name: str
    building_space_fk: bytes

class BuildingRoomCreate(BuildingRoomBase):
    pass

class BuildingRoom(BuildingRoomBase):
    building_room_pk: bytes

    class Config:
        orm_mode: True

# Driver Schemas
class DriverBase(BaseModel):
    driver_type: str

class DriverCreate(DriverBase):
    pass

class Driver(DriverBase):
    driver_pk: bytes

    class Config:
        orm_mode: True

# Device Schemas
class DeviceBase(BaseModel):
    device_name: str
    device_type: str
    driver_fk: bytes
    driver_data: dict
    device_values: dict
    room_fk: bytes

class DeviceCreate(DeviceBase):
    pass

class Device(DeviceBase):
    device_pk: bytes

    class Config:
        orm_mode: True

# Role Schemas
class RoleBase(BaseModel):
    role_name: str
    security_level: int

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    role_pk: bytes

    class Config:
        orm_mode: True

# User Schemas
class UserBase(BaseModel):
    username: str
    full_name: str
    email: str
    fk_role: bytes

class UserCreate(UserBase):
    pass

class User(UserBase):
    user_pk: bytes

    class Config:
        orm_mode: True
