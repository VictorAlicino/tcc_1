"""Room/Space/Building Manager"""
import logging
import json
import traceback
from typing import Any
from uuid import uuid1, UUID
from sqlalchemy.orm import Session
from db import models

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
        self.opus_interfaces = interfaces

        self.load_db()
        self._configure_mqtt(interfaces)
        log.info('Location Manager Initialized.')

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
        if building not in self.buildings:
            raise ValueError(f'{building.name} Building not found.')
        # Check if the name is already in use in this building
        for space in self.spaces.values():
            if space.name == name and space.building == building:
                raise ValueError(f'{space.name} Space name already in use in this building.')
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

    def new_room(self, name: str, space: UUID, building: UUID) -> None:
        """Add a new room"""
        log.debug('Adding new room %s', name)
        new_uuid = uuid1()
        # Check if the provided space exists
        try:
            space = self.spaces[space]
            if space.building != self.get_building(building_id=building).id:
                raise ValueError(f'{space.name} Space not in the provided building.')
        except KeyError as exc:
            exc.args = ('Space not found.',)
        # Check if the name is already in use in this space
        for room in self.rooms.values():
            if room.name == name and room.space == space.id:
                raise ValueError(f'{room.name} Room name already in use in this space.')
        # Check if the UUID is already in use
        while new_uuid in self.rooms:
            new_uuid = uuid1()

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
        log.debug('get_building is looking for building [%s | %s]', name, building_id)
        if building_id:
            return self.buildings[building_id]
        if name:
            for building in self.buildings.values():
                if building.name == name:
                    return building
        raise ValueError('Building not found.')

    def get_space(self,
                  name: str = None,
                  space_id: UUID = None,
                  building_name: str = None,
                  building_id: UUID = None) -> Any | None:
        """Return a space by name or id"""
        log.debug('get_space is looking for space [%s | %s] @ [%s | %s]',
                  name,
                  space_id,
                  building_name,
                  building_id)
        if space_id:
            try:
                return self.spaces[space_id]
            except KeyError as exc:
                exc.args = ('Space not found.',)
        if name and (building_name or building_id):
            candidates = []
            for space in self.spaces.values():
                if space.name == name:
                    candidates.append(space)
            for candidate in candidates:
                if building_name:
                    if self.buildings[candidate.building].name == building_name:
                        return candidate
                if building_id:
                    if candidate.building == building_id:
                        return candidate
        raise ValueError('Space not found.')

    def get_room(self,
                 room_id: UUID = None):
        """Return a room by id"""
        log.debug('get_room is looking for room [%s]', room_id)
        if room_id:
            try:
                return self.rooms[room_id]
            except KeyError as exc:
                exc.args = ('Room not found.',)
                log.error(exc)

    def dump_buildings(self, send_to_log=False) -> None:
        """Print all buildings"""
        if send_to_log:
            log.debug('All buildings in the LocationManager')
            for building in self.buildings.values():
                log.debug('├──Building: %s', building.name)
                log.debug('│\t└── UUID: %s', building.id)
            log.debug('└── ALL BUILDINGS ABOVE')
        dump: dict = {}
        for building in self.buildings.values():
            dump[str(building.id)] = building.name
        return dump

    def dump_spaces(self, send_to_log=False) -> None:
        """Print all spaces"""
        if send_to_log:
            log.debug('All spaces in the LocationManager')
            for space in self.spaces.values():
                log.debug('├──Space: %s', space.name)
                log.debug('│\t├── UUID: %s', space.id)
                log.debug('│\t└── @ Building: %s', self.buildings[space.building].name)
            log.debug('└── ALL SPACES ABOVE')
        dump: dict = {}
        for space in self.spaces.values():
            dump[str(space.id)] = space.name
        return dump

    def dump_rooms(self, send_to_log=False) -> None:
        """Print all rooms"""
        if send_to_log:
            log.debug('All rooms in the LocationManager')
            for room in self.rooms.values():
                log.debug('├──Room: %s', room.name)
                log.debug('│\t├── UUID: %s', room.id)
                log.debug('│\t├── @ Space: %s', self.spaces[room.space].name)
                log.debug('│\t└── @ Building: %s', self.buildings[room.building].name)
            log.debug('└── ALL ROOMS ABOVE')
        dump: dict = {}
        for room in self.rooms.values():
            dump[str(room.id)] = room.name
        return dump

    def _configure_mqtt(self, interfaces: dict) -> None:
        """Configure MQTT Interface for the right Callbacks"""
        log.debug('Configuring MQTT Interface')
        interfaces['mqtt<maestro>'].register_callback('building/#', self._mqtt_callback)
        interfaces['mqtt<maestro>'].register_callback('space/#', self._mqtt_callback)
        interfaces['mqtt<maestro>'].register_callback('room/#', self._mqtt_callback)
        log.debug('MQTT Interface Configured')

    def _mqtt_callback(self, client, userdata, msg):
        """MQTT Callback"""
        log.debug("MQTT Message Received: %s", msg.topic)
        topic = msg.topic.split('/')
        if not msg.payload == b'':
            try:
                payload = json.loads(msg.payload)
            except json.JSONDecodeError:
                log.error('Invalid JSON Received')
                return

        match topic[1]:
            case 'building':
                match topic[2]:
                    case 'new':
                        try:
                            temp = json.loads(msg.payload)
                            self.new_building(temp['name'])
                            self.opus_interfaces['mqtt<local>'].publish(
                                payload['callback'],
                                json.dumps({'status': 'success'})
                            )
                            self.opus_interfaces['mqtt<maestro>'].publish(
                                payload['callback'],
                                json.dumps({'status': 'success'})
                            )
                        except (
                            ValueError,
                            KeyError,
                            json.JSONDecodeError
                            ):
                            log.warning(msg.payload)
                            self.opus_interfaces['mqtt<local>'].publish(
                                payload['callback'],
                                json.dumps({'status': 'failed'})
                            )
                            self.opus_interfaces['mqtt<maestro>'].publish(
                                payload['callback'],
                                json.dumps({'status': 'failed'})
                            )
                    case 'list':
                        self.opus_interfaces['mqtt<local>'].publish(
                            payload['callback'],
                            json.dumps(self.dump_buildings())
                        )
                        self.opus_interfaces['mqtt<maestro>'].publish(
                            payload['callback'],
                            json.dumps(self.dump_buildings())
                        )
            case 'space':
                match topic[2]:
                    case 'new':
                        try:
                            temp = json.loads(msg.payload)
                            self.new_space(
                                temp['name'],
                                self.get_building(temp['building']).id
                            )
                            self.opus_interfaces['mqtt<local>'].publish(
                                payload['callback'],
                                json.dumps({'status': 'success'})
                            )
                            self.opus_interfaces['mqtt<maestro>'].publish(
                                payload['callback'],
                                json.dumps({'status': 'success'})
                            )
                        except (
                            ValueError,
                            KeyError,
                            json.JSONDecodeError
                            ):
                            log.warning(msg.payload)
                            self.opus_interfaces['mqtt<local>'].publish(
                                payload['callback'],
                                json.dumps({'status': 'failed'})
                            )
                            self.opus_interfaces['mqtt<maestro>'].publish(
                                payload['callback'],
                                json.dumps({'status': 'failed'})
                            )
                    case 'list':
                        self.opus_interfaces['mqtt<local>'].publish(
                            payload['callback'],
                            json.dumps(self.dump_spaces())
                        )
                        self.opus_interfaces['mqtt<maestro>'].publish(
                            payload['callback'],
                            json.dumps(self.dump_spaces())
                        )
            case 'room':
                match topic[2]:
                    case 'new':
                        try:
                            temp = json.loads(msg.payload)
                            space = self.get_space(name=temp['space'],
                                                   building_name=temp['building'])
                            self.new_room(
                                temp['name'],
                                space.id,
                                space.building
                            )
                            self.opus_interfaces['mqtt<local>'].publish(
                                payload['callback'],
                                json.dumps({'status': 'success'})
                            )
                            self.opus_interfaces['mqtt<maestro>'].publish(
                                payload['callback'],
                                json.dumps({'status': 'success'})
                            )
                        except (
                            ValueError,
                            KeyError,
                            json.JSONDecodeError,
                            AttributeError):
                            log.warning(msg.payload)
                            self.opus_interfaces['mqtt<local>'].publish(
                                payload['callback'],
                                json.dumps({'status': 'failed'})
                            )
                            self.opus_interfaces['mqtt<maestro>'].publish(
                                payload['callback'],
                                json.dumps({'status': 'failed'})
                            )
                    case 'list':
                        self.opus_interfaces['mqtt<local>'].publish(
                            payload['callback'],
                            json.dumps(self.dump_rooms())
                        )
                        self.opus_interfaces['mqtt<maestro>'].publish(
                            payload['callback'],
                            json.dumps(self.dump_rooms())
                        )
