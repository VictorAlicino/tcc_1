"""CRUD Operations for the database."""
import logging
import uuid
from core.location_manager import Building, Space, Room
from sqlalchemy import UUID
from sqlalchemy.orm import Session
from . import models, schemas

log = logging.getLogger(__name__)

# CREATE

def create_building_on_db(db: Session, building: Building):
    """Create a new building on the database"""
    #db = next(db)
    db_building = models.Building(
        building_pk=building.id,
        building_name=building.name
    )
    db.add(db_building)
    db.commit()
    db.refresh(db_building)
    log.debug('Building %s added to the database.', building.name)

def create_space_on_db(db: Session, space: Space):
    """Create a new space on the database"""
    #db = next(db)
    db_space = models.BuildingSpace(
        building_space_pk=space.id,
        building_fk=space.building,
        space_name=space.name
    )
    db.add(db_space)
    db.commit()
    db.refresh(db_space)
    log.debug('Space %s added to the database.', space.name)

def create_room_on_db(db: Session, room: Room):
    """Create a new room on the database"""
    #db = next(db)
    db_room = models.BuildingRoom(
        building_room_pk=room.id,
        building_space_fk=room.space,
        room_name=room.name
    )
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    log.debug('Room %s added to the database.', room.name)

def assign_new_user(db: Session, user: models.User):
    """Assign a new user coming from Maestro"""
    #db = next(db)
    db.add(user)
    db.commit()
    db.refresh(user)
    log.debug('User %s added to the database', user.given_name)

# READ

def get_user_by_id(db: Session, id: str) -> models.User | None:
    """Get the user by id"""
    #db = next(db)
    id = uuid.UUID(id)
    return db.query(models.User).filter(models.User.user_pk == id).first()

def get_role_by_id(db: Session, security_level: int) -> models.Role | None:
    """Get the role entity by Security Level"""
    #db = next(db)
    return db.query(models.Role).filter(models.Role.security_level == security_level).first()

def get_role_uuid(db: Session, role_pk: str) -> models.Role | None:
    """Get the role entity by name"""
    #db = next(db)
    return db.query(models.Role).filter(models.Role.role_pk == role_pk).first()

def get_role_by_name(db: Session, role_name: str) -> models.Role | None:
    """Get the role entity by name"""
    #db = next(db)
    return db.query(models.Role).filter(models.Role.role_name == role_name).first()

def get_all_devices_authorized_to_a_role(db: Session, role: models.Role) -> list[models.Device]:
    """Get all devices authorized to a role"""
    #db = next(db)
    return db.query(models.Device).join(models.role_device).filter(models.role_device.c.role_pk == role.role_pk).all()
# UPDATE


# DELETE