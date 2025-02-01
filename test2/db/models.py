"""Database models for Opus"""
from sqlalchemy import Table, Column, String, UUID, JSON, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship
from .db import Base

class Building(Base):
    """Building model"""
    __tablename__ = "building"
    building_pk = Column(UUID, primary_key=True, nullable=False)
    building_name = Column(String, nullable=False)

class BuildingSpace(Base):
    """Building space model"""
    __tablename__ = "building_space"
    building_space_pk = Column(UUID, primary_key=True, nullable=False)
    building_fk = Column(UUID, ForeignKey('building.building_pk'), nullable=False)
    space_name = Column(String, nullable=False)
    building = relationship("Building", back_populates="spaces")

class BuildingRoom(Base):
    """Building room model"""
    __tablename__ = "building_room"
    building_room_pk = Column(UUID, primary_key=True, nullable=False)
    building_space_fk = Column(UUID, ForeignKey('building_space.building_space_pk'), nullable=False)
    room_name = Column(String, nullable=False)
    building_space = relationship("BuildingSpace", back_populates="rooms")

#class Driver(Base):
#    """Driver model"""
#    __tablename__ = "drivers"
#    driver_pk = Column(UUID, primary_key=True, nullable=False)
#    driver_type = Column(String, nullable=False)

class Device(Base):
    """Device model"""
    __tablename__ = "device"
    device_pk = Column(UUID, primary_key=True, nullable=False)
    room_fk = Column(UUID, ForeignKey('building_room.building_room_pk'), nullable=False)
    device_name = Column(String, nullable=False)
    device_type = Column(String, nullable=False)
    driver_name = Column(String, nullable=False)
    driver_data = Column(JSON)
    building_room = relationship("BuildingRoom", back_populates="devices")
    # driver = relationship("Driver", back_populates="devices")

class Role(Base):
    """Role model"""
    __tablename__ = "roles"
    role_pk = Column(UUID, primary_key=True, nullable=False)
    role_name = Column(String, nullable=False)
    security_level = Column(SmallInteger, nullable=False)

class User(Base):
    """User model"""
    __tablename__ = "users"
    user_pk = Column(UUID, primary_key=True, nullable=False)
    #username = Column(String, nullable=False, unique=True)
    #full_name = Column(String, nullable=False)
    given_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    fk_role = Column(UUID, ForeignKey('roles.role_pk'), nullable=False)
    role = relationship("Role", back_populates="users")

Building.spaces = relationship(
    "BuildingSpace",
    order_by=BuildingSpace.building_space_pk,
    back_populates="building"
    )
BuildingSpace.rooms = relationship(
    "BuildingRoom",
    order_by=BuildingRoom.building_room_pk,
    back_populates="building_space"
    )
BuildingRoom.devices = relationship(
    "Device",
    order_by=Device.device_pk,
    back_populates="building_room"
    )
#Driver.devices = relationship(
#    "Device",
#    order_by=Device.device_pk,
#    back_populates="driver"
#    )
Role.users = relationship(
    "User",
    order_by=User.user_pk,
    back_populates="role"
    )

role_device = Table(
    "role_device",
    Base.metadata,
    Column("role_pk", UUID, ForeignKey("roles.role_pk"), primary_key=True),
    Column("device_pk", UUID, ForeignKey("device.device_pk"), primary_key=True)
)

