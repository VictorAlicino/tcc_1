"""Room/Space/Building Manager"""
import logging
from uuid import UUID

log = logging.getLogger(__name__)

class Building():
    """Building class"""
    def __init__(self):
        self.id: UUID = None
        self.name: str = None

class Space():
    """Space class"""
    def __init__(self):
        self.id: UUID = None
        self.name: str = None
        self.building: UUID = None

class Room():
    """Room class"""
    def __init__(self):
        self.id: UUID = None
        self.name: str = None
        self.space: UUID = None
        self.building: UUID = None

class LocationManager():
    """Location Manager"""
    def __init__(self):
        self.buildings: list = {}
        self.spaces: list = {}
        self.rooms: list = {}

    def new_building(self, name: str) -> None:
        """Add a new building"""
        new_uuid = UUID()
        # Check if the UUID is already in use
        while new_uuid in self.buildings:
            new_uuid = UUID()

        building = Building()
        building.id = new_uuid
        building.name = name
        self.buildings[building.id] = building

    def new_space(self, name: str, building: UUID) -> None:
        """Add a new space"""
        new_uuid = UUID()
        # Check if the provided building exists
        if building not in self.buildings:
            raise ValueError('Building not found.')
        # Check if the UUID is already in use
        while new_uuid in self.spaces:
            new_uuid = UUID()

        space = Space()
        space.id = new_uuid
        space.name = name
        space.building = building
        self.spaces[space.id] = space

    def new_room(self, name: str, space: UUID) -> None:
        """Add a new room"""
        new_uuid = UUID()
        # Check if the provided space exists
        space: Space = None
        try:
            space = self.spaces[space]
        except KeyError as exc:
            exc.args = ('Space not found.',)
        # Check if the UUID is already in use
        while new_uuid in self.rooms:
            new_uuid = UUID()

        room = Room()
        room.id = new_uuid
        room.name = name
        room.space = space.id
        room.building = space.building
        self.rooms[room.id] = room

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