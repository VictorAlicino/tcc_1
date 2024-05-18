"""Room/Space/Building Manager"""
import logging
from typing import Any
from uuid import uuid1, UUID
from sqlalchemy.orm import Session
from db import models

log = logging.getLogger(__name__)

INTERFACES = {}

class Building:
    """Building class"""
    def __init__(self):
        self.id: UUID
        self.name: str


class Space:
    """Space class"""
    def __init__(self):
        self.id: UUID
        self.name: str
        self.building: UUID


class Room:
    """Room class"""
    def __init__(self):
        self.id: UUID
        self.name: str
        self.space: UUID
        self.building: UUID

def create_building_on_db(db: Session, building: Building):
    """Create a new building on the database"""
    db = next(db)
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
    db = next(db)
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
    db = next(db)
    db_room = models.BuildingRoom(
        building_room_pk=room.id,
        building_space_fk=room.space,
        room_name=room.name
    )
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    log.debug('Room %s added to the database.', room.name)

class LocationManager:
    """Location Manager"""

    def __init__(self, interfaces: dict):
        log.debug('Initializing Location Manager.')
        self.buildings: dict = {}
        self.spaces: dict = {}
        self.rooms: dict = {}
        self.opus_db = interfaces['opus_db']

        self.load_db()

    def new_building(self, name: str) -> None:
        """Add a new building"""
        log.debug('Adding new building %s', name)
        new_uuid = uuid1()
        # Check if the UUID is already in use
        while new_uuid in self.buildings:
            new_uuid = uuid1()
        # Check if the name is already in use
        for building in self.buildings.values():
            if building.name == name:
                raise ValueError(f'{building.name} Building name already in use.')
        building = Building()
        building.id = new_uuid
        building.name = name
        self.buildings[building.id] = building
        create_building_on_db(self.opus_db.get_db(), building)
        log.debug('New Building Added')
        log.debug('└─── Building: %s', building.name)
        log.debug('     └── UUID: %s', building.id)

    def new_space(self, name: str, building: UUID) -> None:
        """Add a new space"""
        log.debug('Adding new space %s', name)
        new_uuid = uuid1()
        # Check if the provided building exists
        print(self.buildings)
        if building not in self.buildings:
            raise ValueError(f'{building.name} Building not found.')
        # Check if the name is already in use
        for space in self.spaces.values():
            if space.name == name:
                raise ValueError(f'{space.name} Space name already in use.')
        # Check if the UUID is already in use
        while new_uuid in self.spaces:
            new_uuid = uuid1()

        space = Space()
        space.id = new_uuid
        space.name = name
        space.building = building
        self.spaces[space.id] = space
        create_space_on_db(self.opus_db.get_db(), space)
        log.debug('New Space Added')
        log.debug('└─── Space: %s', space.name)
        log.debug('     ├── UUID: %s', space.id)
        log.debug('     └── Building: %s | %s',
                  self.buildings[space.building].name,
                  self.buildings[space.building].id)

    def new_room(self, name: str, space: UUID) -> None:
        """Add a new room"""
        log.debug('Adding new room %s', name)
        new_uuid = uuid1()
        # Check if the provided space exists
        try:
            space = self.spaces[space]
        except KeyError as exc:
            exc.args = ('Space not found.',)
        # Check if the UUID is already in use
        while new_uuid in self.rooms:
            new_uuid = uuid1()
        # Check if the name is already in use
        for room in self.rooms.values():
            if room.name == name:
                raise ValueError(f'{room.name} Room name already in use.')

        room = Room()
        room.id = new_uuid
        room.name = name
        room.space = space.id
        room.building = space.building
        self.rooms[room.id] = room
        create_room_on_db(self.opus_db.get_db(), room)
        log.debug('New Room Added')
        log.debug('└─── Room: %s', room.name)
        log.debug('     ├── UUID: %s', room.id)
        log.debug('     ├── Space: %s | %s',
                  self.spaces[room.space].name,
                  self.spaces[room.space].id)
        log.debug('     └── Building: %s | %s',
                  self.buildings[room.building].name,
                  self.buildings[room.building].id)

    def load_db(self) -> None:
        """Load all locations from the database"""
        log.debug('Loading locations from the database.')
        self._load_buildings_from_db()
        log.debug('└─── Buildings loaded')
        self._load_spaces_from_db()
        log.debug('     └─── Spaces loaded')
        self._load_rooms_from_db()
        log.debug('          └─── Rooms loaded')
        log.debug('Locations loaded from the database.')

    def _load_buildings_from_db(self) -> None:
        """Load buildings from the database"""
        db = next(self.opus_db.get_db())
        db.query(models.Building).all()
        for building in db.query(models.Building).all():
            new_building = Building()
            new_building.id = building.building_pk
            new_building.name = building.building_name
            self.buildings[new_building.id] = new_building
        db.close()

    def _load_spaces_from_db(self) -> None:
        """Load spaces from the database"""
        db = next(self.opus_db.get_db())
        db.query(models.BuildingSpace).all()
        for space in db.query(models.BuildingSpace).all():
            new_space = Space()
            new_space.id = space.building_space_pk
            new_space.name = space.space_name
            new_space.building = space.building_fk
            self.spaces[new_space.id] = new_space
        db.close()

    def _load_rooms_from_db(self) -> None:
        """Load rooms from the database"""
        db = next(self.opus_db.get_db())
        db.query(models.BuildingRoom).all()
        for room in db.query(models.BuildingRoom).all():
            new_room = Room()
            new_room.id = room.building_room_pk
            new_room.name = room.room_name
            new_room.space = room.building_space_fk
            new_room.building = self.spaces[new_room.space].building
            self.rooms[new_room.id] = new_room
        db.close()

    def get_building(self, name: str = None,
                     building_id: UUID = None) -> Any | None:
        """Return a building by name or id"""
        if building_id:
            return self.buildings[building_id]
        if name:
            for building in self.buildings.values():
                if building.name == name:
                    return building
        return None

    def get_space(self, name: str = None,
                  space_id: UUID = None) -> Any | None:
        """Return a space by name or id"""
        if space_id:
            return self.spaces[space_id]
        if name:
            for space in self.spaces.values():
                if space.name == name:
                    return space
        return None

    def dump_buildings(self) -> None:
        """Print all buildings"""
        log.debug('All buildings in the location manager')
        for building in self.buildings.values():
            log.debug('├──Building: %s', building.name)
            log.debug('│\t└── UUID: %s', building.id)
        log.debug('└── ALL BUILDINGS ABOVE')

    def dump_spaces(self) -> None:
        """Print all spaces"""
        log.debug('All spaces in the location manager')
        for space in self.spaces.values():
            log.debug('├──Space: %s', space.name)
            log.debug('│\t├── UUID: %s', space.id)
            log.debug('│\t└── @ Building: %s', self.buildings[space.building].name)
        log.debug('└── ALL SPACES ABOVE')

    def dump_rooms(self) -> None:
        """Print all rooms"""
        log.debug('All rooms in the location manager')
        for room in self.rooms.values():
            log.debug('├──Room: %s', room.name)
            log.debug('│\t├── UUID: %s', room.id)
            log.debug('│\t├── @ Space: %s', self.spaces[room.space].name)
            log.debug('│\t└── @ Building: %s', self.buildings[room.building].name)
        log.debug('└── ALL ROOMS ABOVE')
