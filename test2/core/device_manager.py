"""Devices Manager"""
import os
import logging
import json
from uuid import UUID
from sqlalchemy.orm import Session
from db import models
from .devices import hvac, light

log = logging.getLogger(__name__)

def create_device_on_db(db: Session, device: any) -> None:
    """Create a Device in the database"""
    log.debug('Creating Device in the database')
    db = next(db)
    db_device = models.Device(
        device_pk=device.id,
        room_fk=device.room_id,
        device_name=device.name,
        device_type=device.type,
        driver_name=device.driver
    )
    match device.driver:
        case 'sonoff':
            db_device.driver_data = {
                'id': str(device.id),
                'ip_address': str(device.ip_address),
                'hostname': device.hostname,
                'port': device.port,
                'device_id': device.device_id,
                'bssid': device.bssid,
                'startup_info_dump': device.startup_info_dump,
                'device_type': device.type
            }
        case 'tasmota':
            db_device.driver_data = {
                'id': str(device.id),
                'tasmota_name': device.mqtt_name,
                'device_type': device.type
            }
        case _:
            log.error('Driver not found')
            log.error('Device not created in the database')
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    log.info('Device Created in the database')

class DeviceManager:
    """Devices Manager"""

    def __init__(self,
                 dirs: dict,
                 interfaces: dict,
                 drivers: dict,
                 location_manager: any) -> None:
        log.debug('Initializing Device Manager.')
        self.devices: dict = {}  # This is gonna be hella big
        self.available_devices: dict = {}  # This is gonna be worse
        self.opus_db = interfaces['opus_db']
        self.opus_drivers = drivers
        self.location_manager = location_manager
        #self._load_devices_from_db()

        self._manager_init(dirs)
        self._configure_mqtt(interfaces)
        log.info('Device Manager initialized.')

    def _manager_init(self, dirs: dict) -> None:
        """Initialize Device Manager in-memory database"""
        log.debug('Initializing Device Manager in-memory database.')
        for device_type in os.listdir(f'{dirs['CORE']}/devices'):
            if device_type.endswith('.py') and not device_type.startswith('__'):
                log.debug('Creating virtual db for %s', device_type[:-3])
                self.devices[f'opus_{device_type[:-3]}'] = {}
        log.debug('Device Manager in-memory database initialized.')

    def new_device(self, device) -> None:
        """Add a new device to available devices"""
        log.debug('Adding new available device.')
        if f'{device.driver}' not in self.available_devices:
            self.available_devices[f'{device.driver}'] = []
        self.available_devices[f'{device.driver}'].append(device)
        log.debug('└── New Device Available %s',
                  device)
        log.debug('   ├── Device Type: %s', device.type)
        log.debug('   └── Device Driver: %s', device.driver)

    def register_device(self,
                        device_id: UUID,
                        device_name: str,
                        device_driver: str,
                        room_id: UUID) -> None:
        """Register a device in the device manager"""
        log.debug("Registering a new device")
        log.debug("├── Device ID: %s", device_id)
        log.debug("├── Device Driver: %s", device_driver)
        log.debug("└── Room ID: %s", room_id)
        new_device = None
        # Check if the device is available
        for available_device in self.available_devices[device_driver]:
            if available_device.id == device_id:
                new_device = available_device
        if new_device is None:
            raise ValueError('Device not found in available devices')
        # Check if the room is available
        if room_id not in self.location_manager.rooms:
            raise ValueError('Room not found in available rooms')
        match new_device.type:
            case 'LIGHT':
                temp_device = (
                    self.opus_drivers[device_driver]
                    .new_light(device_name, new_device)
                )
                temp_room = self.location_manager.get_room(room_id)
                temp_device.room_id = temp_room.id
                temp_device.space_id = temp_room.space
                temp_device.building_id = temp_room.building
                self.devices['opus_light'][device_id] = temp_device
                log.info('New Light Registered:')
                self.devices['opus_light'][device_id].print_data()
            case 'HVAC':
                temp_device = (
                    self.opus_drivers[device_driver]
                    .new_hvac(device_name, new_device)
                )
                temp_room = self.location_manager.get_room(room_id)
                temp_device.room_id = temp_room.id
                temp_device.space_id = temp_room.space
                temp_device.building_id = temp_room.building
                self.devices['opus_hvac'][device_id] = temp_device
                log.info('New HVAC Registered:')
                self.devices['opus_hvac'][device_id].print_data()
            case _:
                log.error('Device Type not found')
        self.available_devices[device_driver].remove(new_device)
        create_device_on_db(self.opus_db.get_db(), temp_device)

    def get_available_devices(self) -> list:
        """Return all available devices"""
        return self.available_devices

    def get_device(self, device_id: UUID) -> any:
        """Return a device"""
        try:
            for device_type in self.devices.items():
                for device in self.devices[device_type]:
                    return self.devices[device_type][device]
        except KeyError:
            log.error('Device not found')

    def dump_devices(self) -> None:
        """Print all devices"""
        log.debug('All devices in the DeviceManager')
        log.debug('├──REGISTERED DEVICES')
        for device_type, devices in self.devices.items():
            log.debug('│\t├── %s', device_type)
            for device in devices:
                log.debug('│\t│\t├── %s', device)
            log.debug('│\t│\t└── END OF %s', device_type)
        log.debug('│\t└── END OF REGISTERED DEVICES')
        log.debug('└──AVAILABLE DEVICES')
        for device_type, devices in self.available_devices.items():
            log.debug('\t├── %s', device_type)
            for device in devices:
                log.debug('\t│\t├── %s', device)
            log.debug('\t│\t└── END OF %s', device_type)
        log.debug('\t└── END OF AVAILABLE DEVICES')

    def dump_available_devices(self) -> None:
        """Print all available devices"""
        log.debug('All available devices in the DeviceManager')
        for driver, devices in self.available_devices.items():
            log.debug('├── %s', driver)
            for device in devices:
                log.debug('│\t├── %s : %s', device.id, device.type)
            log.debug('│\t└── END OF %s', driver)
        log.debug('└── END OF AVAILABLE DEVICES')

    def dump_drivers(self) -> None:
        """Print all drivers"""
        log.debug('All drivers in the DeviceManager')
        for driver, _ in self.opus_drivers.items():
            log.debug('├── %s', driver)
        log.debug('└── END OF DRIVERS')

    def load_devices_from_db(self) -> None:
        """Load all devices from the database"""
        log.debug('Loading all devices from the database')
        db = self.opus_db.get_db()
        db = next(db)
        for device in db.query(models.Device).all():
            match device.device_type: 
                case 'LIGHT':
                    temp_device = (
                        self.opus_drivers[device.driver_name]
                        .load_light(device.device_name, device.driver_data)
                    )
                    temp_device.room_id = device.room_fk
                    temp_room = self.location_manager.get_room(device.room_fk)
                    temp_device.space_id = temp_room.space
                    temp_device.building_id = temp_room.building
                    self.devices['opus_light'][device.device_pk] = temp_device
                case 'HVAC':
                    temp_device = (
                        self.opus_drivers[device.driver_name]
                        .load_hvac(device.device_name, device.driver_data)
                    )
                    temp_device.room_id = device.room_fk
                    temp_room = self.location_manager.get_room(device.room_fk)
                    temp_device.space_id = temp_room.space
                    temp_device.building_id = temp_room.building
                    self.devices['opus_hvac'][device.device_pk] = temp_device
                case _:
                    log.error('Device Type not found')
        log.info('All devices loaded from the database')
        db.close()

    def _configure_mqtt(self, interfaces: dict) -> None:
        """Configure MQTT"""
        log.debug('Configuring MQTT for DeviceManager.')
        interfaces['mqtt<local>'].register_callback('devices/#', self._mqtt_callback)
        interfaces['mqtt<maestro>'].register_callback('devices/#', self._mqtt_callback)
        log.debug('MQTT Configured for Device Manager.')

    def _mqtt_callback(self, client, userdata, msg):
        """MQTT Callback"""
        log.debug("MQTT Message Received: %s", msg.topic)
        topic = msg.topic.split('/')
        if topic[1] == 'devices':
            match topic[2]:
                case 'list_all':
                    self.dump_devices()
                case 'all_drivers':
                    self.dump_drivers()
                case 'available':
                    self.dump_available_devices()
                case 'register':
                    try:
                        temp = json.loads(msg.payload)
                        print(temp)
                        self.register_device(
                            device_id=UUID(temp['id']),
                            device_name=temp['name'],
                            device_driver=temp['driver'],
                            room_id=UUID(temp['room_id']))
                    except (ValueError, json.JSONDecodeError) as exc:
                        log.warning(msg.payload)
                        log.error(exc)
            if topic[2] in self.opus_drivers:
                try:
                    log.debug("Driver specific message received, sending to %s.", topic[2])
                    self.opus_drivers[topic[2]]._mqtt_callback(topic, json.loads(msg.payload)) # pylint: disable=protected-access
                except json.JSONDecodeError:
                    log.error('Invalid JSON Received')
            else:
                try:
                    device_id = UUID(topic[2])
                    device = self.get_device(device_id)
                    self._device_command(device, json.loads(msg.payload))
                except ValueError:
                    log.error('Invalid Command Received')

    def _device_command(self, device, command: json) -> None:
        """Receive a command from MQTT"""
        log.debug('Device Command Received')
        log.debug('├── Device ID: %s', device.id)
        log.debug('└──> Command: %s', command)
        match command['cmnd']:
            case "on":
                device.on()
            case "off":
                device.off()
            case "toggle":
                device.toggle()
