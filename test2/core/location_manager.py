"""Room/Space/Building Manager"""
import logging
import sqlite3
from typing import Any
from uuid import uuid1, UUID

log = logging.getLogger(__name__)


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


class LocationManager:
    """Location Manager"""

    def __init__(self, dirs: dict):
        log.debug('Initializing Location Manager.')
        self.buildings: dict = {}
        self.spaces: dict = {}
        self.rooms: dict = {}

        log.debug('Connecting to the local database.')
        self.db_conn = sqlite3.connect(f'{dirs['DATABASES']}/opus-vault.db')  # Persistent database
        with open(f'{dirs['DATABASES']}/create_db.sql', 'r', encoding='utf-8') as f:
            c = self.db_conn.cursor()
            c.executescript(f.read())

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
                raise ValueError('Building name already in use.')

        building = Building()
        building.id = new_uuid
        building.name = name
        self.buildings[building.id] = building
        db = self.db_conn.cursor()
        db.execute("""
            INSERT INTO building (building_pk, building_name)
                   VALUES (?, ?)""",
            (building.id.bytes, building.name)
        )
        log.debug('New Building Added')
        log.debug('└─── Building: %s', building.name)
        log.debug('     └── UUID: %s', building.id)
        self.db_conn.commit()

    def new_space(self, name: str, building: UUID) -> None:
        """Add a new space"""
        log.debug('Adding new space %s', name)
        new_uuid = uuid1()
        # Check if the provided building exists
        if building not in self.buildings:
            raise ValueError('Building not found.')
        # Check if the name is already in use
        for space in self.spaces.values():
            if space.name == name:
                raise ValueError('Space name already in use.')
        # Check if the UUID is already in use
        while new_uuid in self.spaces:
            new_uuid = uuid1()

        space = Space()
        space.id = new_uuid
        space.name = name
        space.building = building
        self.spaces[space.id] = space
        db = self.db_conn.cursor()
        db.execute("""
            INSERT INTO building_space (building_space_pk, space_name, building_fk)
            VALUES (?, ?, ?)""",
            (space.id.bytes, space.name, space.building.bytes)
        )
        log.debug('New Space Added')
        log.debug('└─── Space: %s', space.name)
        log.debug('     ├── UUID: %s', space.id)
        log.debug('     └── Building: %s | %s',
                  self.buildings[space.building].name,
                  self.buildings[space.building].id)
        self.db_conn.commit()

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
                raise ValueError('Room name already in use.')

        room = Room()
        room.id = new_uuid
        room.name = name
        room.space = space.id
        room.building = space.building
        self.rooms[room.id] = room
        db = self.db_conn.cursor()
        db.execute("""INSERT INTO building_room (building_room_pk, room_name, building_space_fk)
                   VALUES (?, ?, ?)""",
            (room.id.bytes, room.name, room.space.bytes)
        )
        log.debug('New Room Added')
        log.debug('└─── Room: %s', room.name)
        log.debug('     ├── UUID: %s', room.id)
        log.debug('     ├── Space: %s | %s',
                  self.spaces[room.space].name,
                  self.spaces[room.space].id)
        log.debug('     └── Building: %s | %s',
                  self.buildings[room.building].name,
                  self.buildings[room.building].id)
        self.db_conn.commit()

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
        db = self.db_conn.cursor()
        db.execute('SELECT * FROM building')
        for row in db.fetchall():
            building = Building()
            building.id = UUID(bytes=row[0])
            building.name = row[1]
            self.buildings[building.id] = building

    def _load_spaces_from_db(self) -> None:
        """Load spaces from the database"""
        db = self.db_conn.cursor()
        db.execute('SELECT * FROM building_space')
        for row in db.fetchall():
            space = Space()
            space.id = UUID(bytes=row[0])
            space.name = row[1]
            space.building = UUID(bytes=row[1])
            self.spaces[space.id] = space

    def _load_rooms_from_db(self) -> None:
        """Load rooms from the database"""
        db = self.db_conn.cursor()
        db.execute('SELECT * FROM building_room')
        for row in db.fetchall():
            room = Room()
            room.id = UUID(bytes=row[0])
            room.name = row[1]
            room.space = UUID(bytes=row[1])
            room.building = self.spaces[room.space].building
            self.rooms[room.id] = room

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
