"""CRUD Operations for the database."""
from sqlalchemy.orm import Session
from . import models, schemas

def db_create_building(db: Session, building: schemas.BuildingCreate):
    """Create a new building"""
    db_building = models.Building(**building.model_dump())
    db.add(db_building)
    db.commit()
    db.refresh(db_building)
    return db_building
