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
        name=device.name,
        id=device.id,
        room_id=device.room_id,
        space_id=device.space_id,
        building_id=device.building_id,
        driver=device.driver,
        type=device.type
    )
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
                self.devices['opus_hvac'][device_id] = (
                    self.opus_drivers[device_driver]
                    .new_hvac(new_device, device_name)
                )
        self.available_devices[device_driver].remove(new_device)


    def get_available_devices(self) -> list:
        """Return all available devices"""
        return self.available_devices

    def dump_devices(self) -> None:
        """Print all devices"""
        log.debug('All devices in the DeviceManager')
        log.debug('├──REGISTERED DEVICES')
        for device_type, devices in self.devices.items():
            log.debug('│\t├── %s: %s', device_type, devices)
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
            if topic[2] == 'list_all':
                self.dump_devices()
            if topic[2] == 'all_drivers':
                self.dump_drivers()
            if topic[2] == 'available':
                self.dump_available_devices()
            if topic[2] == 'register':
                try:
                    temp = json.loads(msg.payload)
                    self.register_device(
                        device_id=UUID(temp['id']),
                        device_name=temp['name'],
                        device_driver=temp['driver'],
                        room_id=UUID(temp['room_id']))
                except (ValueError, json.JSONDecodeError) as exc:
                    log.warning(msg.payload)
                    log.error(exc)
