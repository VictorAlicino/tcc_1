"""Root for API Server"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import schemas, models
from db.db import get_db

router = APIRouter()

# Building Routes
@router.post("/buildings/", response_model=schemas.Building)
def create_building(building: schemas.BuildingCreate, db: Session = Depends(get_db)):
    """Create a new building"""
    return crud.create_building(db=db, building=building)

@router.get("/buildings/", response_model=List[schemas.Building])
def read_buildings(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Read all buildings"""
    buildings = crud.get_buildings(db, skip=skip, limit=limit)
    return buildings

@router.get("/buildings/{building_pk}", response_model=schemas.Building)
def read_building(building_pk: str, db: Session = Depends(get_db)):
    """Read a building by primary key"""
    building = crud.get_building(db, building_pk=building_pk)
    if building is None:
        raise HTTPException(status_code=404, detail="Building not found")
    return building

@router.delete("/buildings/{building_pk}", response_model=schemas.Building)
def delete_building(building_pk: str, db: Session = Depends(get_db)):
    """Delete a building by primary key"""
    building = crud.delete_building(db, building_pk=building_pk)
    if building is None:
        raise HTTPException(status_code=404, detail="Building not found")
    return building

# BuildingSpace Routes
@router.post("/spaces/", response_model=schemas.BuildingSpace)
def create_building_space(space: schemas.BuildingSpaceCreate,
                          db: Session = Depends(get_db)):
    """Create a new building space"""
    return crud.create_building_space(db=db, space=space)

@router.get("/spaces/", response_model=List[schemas.BuildingSpace])
def read_building_spaces(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Read all building spaces"""
    spaces = crud.get_building_spaces(db, skip=skip, limit=limit)
    return spaces

@router.get("/spaces/{space_pk}", response_model=schemas.BuildingSpace)
def read_building_space(space_pk: str, db: Session = Depends(get_db)):
    """Read a building space by primary key"""
    space = crud.get_building_space(db, space_pk=space_pk)
    if space is None:
        raise HTTPException(status_code=404, detail="Building space not found")
    return space

@router.delete("/spaces/{space_pk}", response_model=schemas.BuildingSpace)
def delete_building_space(space_pk: str, db: Session = Depends(get_db)):
    """Delete a building space by primary key"""
    space = crud.delete_building_space(db, space_pk=space_pk)
    if space is None:
        raise HTTPException(status_code=404, detail="Building space not found")
    return space

# BuildingRoom Routes
@router.post("/rooms/", response_model=schemas.BuildingRoom)
def create_building_room(room: schemas.BuildingRoomCreate,
                         db: Session = Depends(get_db)):
    """Create a new building room"""
    return crud.create_building_room(db=db, room=room)

@router.get("/rooms/", response_model=List[schemas.BuildingRoom])
def read_building_rooms(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Read all building rooms"""
    rooms = crud.get_building_rooms(db, skip=skip, limit=limit)
    return rooms

@router.get("/rooms/{room_pk}", response_model=schemas.BuildingRoom)
def read_building_room(room_pk: str, db: Session = Depends(get_db)):
    """Read a building room by primary key"""
    room = crud.get_building_room(db, room_pk=room_pk)
    if room is None:
        raise HTTPException(status_code=404, detail="Building room not found")
    return room

@router.delete("/rooms/{room_pk}", response_model=schemas.BuildingRoom)
def delete_building_room(room_pk: str, db: Session = Depends(get_db)):
    """Delete a building room by primary key"""
    room = crud.delete_building_room(db, room_pk=room_pk)
    if room is None:
        raise HTTPException(status_code=404, detail="Building room not found")
    return room

# Driver Routes
@router.post("/drivers/", response_model=schemas.Driver)
def create_driver(driver: schemas.DriverCreate, db: Session = Depends(get_db)):
    """Create a new driver"""
    return crud.create_driver(db=db, driver=driver)

@router.get("/drivers/", response_model=List[schemas.Driver])
def read_drivers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Read all drivers"""
    drivers = crud.get_drivers(db, skip=skip, limit=limit)
    return drivers

@router.get("/drivers/{driver_pk}", response_model=schemas.Driver)
def read_driver(driver_pk: str, db: Session = Depends(get_db)):
    """Read a driver by primary key"""
    driver = crud.get_driver(db, driver_pk=driver_pk)
    if driver is None:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver

@router.delete("/drivers/{driver_pk}", response_model=schemas.Driver)
def delete_driver(driver_pk: str, db: Session = Depends(get_db)):
    """Delete a driver by primary key"""
    driver = crud.delete_driver(db, driver_pk=driver_pk)
    if driver is None:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver

# Device Routes
@router.post("/devices/", response_model=schemas.Device)
def create_device(device: schemas.DeviceCreate, db: Session = Depends(get_db)):
    """Create a new device"""
    return crud.create_device(db=db, device=device)

@router.get("/devices/", response_model=List[schemas.Device])
def read_devices(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Read all devices"""
    devices = crud.get_devices(db, skip=skip, limit=limit)
    return devices

@router.get("/devices/{device_pk}", response_model=schemas.Device)
def read_device(device_pk: str, db: Session = Depends(get_db)):
    """Read a device by primary key"""
    device = crud.get_device(db, device_pk=device_pk)
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

@router.delete("/devices/{device_pk}", response_model=schemas.Device)
def delete_device(device_pk: str, db: Session = Depends(get_db)):
    """Delete a device by primary key"""
    device = crud.delete_device(db, device_pk=device_pk)
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

# Role Routes
@router.post("/roles/", response_model=schemas.Role)
def create_role(role: schemas.RoleCreate, db: Session = Depends(get_db)):
    """Create a new role"""
    return crud.create_role(db=db, role=role)

@router.get("/roles/", response_model=List[schemas.Role])
def read_roles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Read all roles"""
    roles = crud.get_roles(db, skip=skip, limit=limit)
    return roles

@router.get("/roles/{role_pk}", response_model=schemas.Role)
def read_role(role_pk: str, db: Session = Depends(get_db)):
    """Read a role by primary key"""
    role = crud.get_role(db, role_pk=role_pk)
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.delete("/roles/{role_pk}", response_model=schemas.Role)
def delete_role(role_pk: str, db: Session = Depends(get_db)):
    """Delete a role by primary key"""
    role = crud.delete_role(db, role_pk=role_pk)
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

# User Routes
@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    return crud.create_user(db=db, user=user)

@router.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Read all users"""
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/users/{user_pk}", response_model=schemas.User)
def read_user(user_pk: str, db: Session = Depends(get_db)):
    """Read a user by primary key"""
    user = crud.get_user(db, user_pk=user_pk)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/users/{user_pk}", response_model=schemas.User)
def delete_user(user_pk: str, db: Session = Depends(get_db)):
    """Delete a user by primary key"""
    user = crud.delete_user(db, user_pk=user_pk)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
