"""Devices Manager"""
import os
import logging
import json
import traceback
from types import NoneType
from uuid import UUID
from sqlalchemy.orm import Session
from db import models
import db.crud as crud
import core

log = logging.getLogger(__name__)

def create_device_on_db(db: Session, device: any) -> None:
    """Create a Device in the database"""
    log.debug('Creating Device in the database')
    #db = next(db)
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
                'device_type': device.type,
                'vendor': device.vendor
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
                 managers: any) -> None:
        log.debug('Initializing Device Manager.')
        self.devices: dict = {}  # This is gonna be hella big
        self.available_devices: dict = {}  # This is gonna be worse
        self.opus_db = interfaces['opus_db']
        self.opus_drivers = drivers
        self.location_manager: core.LocationManager = managers['locations']
        self.opus_interfaces = interfaces
        #self._load_devices_from_db()
        self.users_managers: core.UserManager = managers['users']
        self._manager_init(dirs)
        self._configure_mqtt()
        log.info('Device Manager initialized.')

    def _manager_init(self, dirs: dict) -> None:
        """Initialize Device Manager in-memory database"""
        log.debug('Initializing Device Manager in-memory database.')
        for device_type in os.listdir(f"{dirs['CORE']}/devices"):
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
                        room_id: UUID,
                        additional_data=None) -> None:
        """Register a device in the device manager"""
        log.debug("Registering a new device")
        log.debug("\t├── Device ID: %s", device_id)
        log.debug("\t├── Device Driver: %s", device_driver)
        log.debug("\t└── Room ID: %s", room_id)
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
                    .new_hvac(device_name, new_device, additional_data)
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
        db = next(self.opus_db.get_db())
        try:
            create_device_on_db(db, temp_device)
        finally:
            db.close()

    def get_available_devices(self) -> list:
        """Return all available devices"""
        return self.available_devices

    def get_device(self, device_id: UUID) -> any:
        """Return a device"""
        try:
            for device_type, devices in self.devices.items(): # pylint: disable=unused-variable
                for device in devices.values():
                    if device.id == device_id:
                        return device
        except KeyError:
            log.error('Device not found')

    def dump_devices(self, send_to_log=False) -> None:
        """Print all devices"""
        send_to_log = True
        if send_to_log:
            log.debug('All devices in the DeviceManager')
            log.debug('├──REGISTERED DEVICES')
            for device_type, devices in self.devices.items():
                log.debug('│\t├── %s', device_type)
                for device in devices:
                    log.debug(f'│\t│\t├── {device} from [{self.devices[device_type][device].driver}]')
                log.debug('│\t│\t└── END OF %s', device_type)
            log.debug('│\t└── END OF REGISTERED DEVICES')
            log.debug('└──AVAILABLE DEVICES')
            for driver, devices in self.available_devices.items():
                for device in devices:
                    log.debug('│\t│\t├── %s : %s', device.id, device.type)
                log.debug('│\t└── END OF %s', driver)
            log.debug(' \t└── END OF AVAILABLE DEVICES')
        dump: dict = {}
        dump['registered_devices'] = {}
        for device_type, devices in self.devices.items():
            dump['registered_devices'][device_type] = {}
            for device in devices:
                dump['registered_devices'][device_type][str(device)] = (
                    self.devices[device_type][device].name)
        dump['available_devices'] = {}
        for driver, devices in self.available_devices.items():
            dump['available_devices'][driver] = {}
            for device in devices:
                dump['available_devices'][driver][str(device)] = device.type
        return dump

    def dump_registered_devices(self, send_to_log=False) -> None:
        """Print all registered devices"""
        if send_to_log:
            log.debug('All registered devices in the DeviceManager')
            for device_type, devices in self.devices.items():
                log.debug('├── %s', device_type)
                for device in devices:
                    log.debug('│\t├── %s', device)
                log.debug('│\t└── END OF %s', device_type)
            log.debug('└── END OF REGISTERED DEVICES')
        dump: dict = {}
        for device_type, devices in self.devices.items():
            dump[device_type] = {}
            for device in devices:
                dump[device_type][str(device)] = self.devices[device_type][device].name
        return dump

    def dump_available_devices(self, send_to_log=False) -> None:
        """Print all available devices"""
        if send_to_log:
            log.debug('All available devices in the DeviceManager')
            for driver, devices in self.available_devices.items():
                log.debug('├── %s', driver)
                for device in devices:
                    log.debug('│\t├── %s : %s', device.id, device.type)
                log.debug('│\t└── END OF %s', driver)
            log.debug('└── END OF AVAILABLE DEVICES')
        dump: dict = {}
        for driver, devices in self.available_devices.items():
            dump[driver] = {}
            for device in devices:
                dump[driver][str(device.id)] = device.type
        return dump

    def dump_drivers(self, send_to_log=False) -> None:
        """Print all drivers"""
        if send_to_log:
            log.debug('All drivers in the DeviceManager')
            for driver, _ in self.opus_drivers.items():
                log.debug('├── %s', driver)
            log.debug('└── END OF DRIVERS')
        dump: list = []
        for driver, _ in self.opus_drivers.items():
            dump.append(driver)
        return dump

    def load_devices_from_db(self) -> None:
        """Load all devices from the database"""
        log.debug('Loading all devices from the database')
        db = next(self.opus_db.get_db())
        try:
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
        finally:
            db.close()

    def link_device_to_roles(self, device: any, roles_names: list[str]) -> None:
        """Link a device to roles"""
        log.debug('Linking device to roles')
        db = next(self.opus_db.get_db())
        try:
            for role_name in roles_names:
                role = crud.get_role_by_name(db, role_name)
                if not role:
                    log.warning(f'Role {role_name} does not exists, ignoring')
                    continue
                crud.authorize_device_to_role(db, device, role)
        finally:
            db.close()

    def _configure_mqtt(self) -> None:
        """Configure MQTT"""
        log.debug('Configuring MQTT for DeviceManager.')
        self.opus_interfaces['mqtt<local>'].register_callback('devices/#', self._mqtt_callback)
        self.opus_interfaces['mqtt<maestro>'].register_callback('devices/#', self._mqtt_callback)
        log.debug('MQTT Configured for Device Manager.')

    def _mqtt_callback(self, client, userdata, msg): # pylint: disable=unused-argument
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
            case 'devices':
                match topic[2]:
                    case 'list_all':
                        data = json.dumps(self.dump_devices())
                        self.opus_interfaces['mqtt<local>'].publish(
                            payload['callback'],
                            data
                            )
                        self.opus_interfaces['mqtt<maestro>'].publish(
                            payload['callback'],
                            data
                            )
                        return
                    case 'list':
                        self.opus_interfaces['mqtt<local>'].publish(
                            payload['callback'],
                            json.dumps(self.dump_registered_devices())
                            )
                        self.opus_interfaces['mqtt<maestro>'].publish(
                            payload['callback'],
                            json.dumps(self.dump_registered_devices())
                            )
                        return
                    case 'all_drivers':
                        self.opus_interfaces['mqtt<local>'].publish(
                            payload['callback'],
                            json.dumps(self.dump_drivers())
                            )
                        self.opus_interfaces['mqtt<maestro>'].publish(
                            payload['callback'],
                            json.dumps(self.dump_drivers())
                            )
                        return
                    case 'available':
                        self.opus_interfaces['mqtt<local>'].publish(
                            payload['callback'],
                            json.dumps(self.dump_available_devices())
                            )
                        self.opus_interfaces['mqtt<maestro>'].publish(
                            payload['callback'],
                            json.dumps(self.dump_available_devices())
                            )
                        return
                    case 'list':
                        try:
                            temp = json.loads(msg.payload)
                            print(temp)
                            self.register_device(
                                device_id=UUID(temp['id']),
                                device_name=temp['name'],
                                device_driver=temp['driver'],
                                room_id=UUID(temp['room_id']))
                            return
                        except (ValueError, json.JSONDecodeError) as exc:
                            log.warning(msg.payload)
                            log.error(exc)
                    case 'register':
                        try:
                            temp = json.loads(msg.payload)
                            self.register_device(
                                device_id=UUID(temp['id']),
                                device_name=temp['name'],
                                device_driver=temp['driver'],
                                room_id=UUID(temp['room_id']))
                            self.link_device_to_roles(
                                self.get_device(UUID(temp['id'])),
                                [
                                    'Administator',
                                    'User',
                                    'Guest'
                                ]
                            )
                            self.opus_interfaces['mqtt<local>'].publish(
                                payload['callback'],
                                json.dumps({'status': 'success'})
                            )
                            self.opus_interfaces['mqtt<maestro>'].publish(
                                payload['callback'],
                                json.dumps({'status': 'success'})
                            )
                            return
                        except Exception as exc: # pylint: disable=broad-except
                            log.warning(msg.payload)
                            self.opus_interfaces['mqtt<maestro>'].publish(
                                payload['callback'],
                                json.dumps({
                                    'status': 'failed',
                                    'reason': str(exc)
                                })
                            )
                            self.opus_interfaces['mqtt<local>'].publish(
                                payload['callback'],
                                json.dumps({
                                    'status': 'failed',
                                    'reason': str(exc)
                                })
                            )
                            return
                    case 'get':
                        try:
                            device = self.get_device(UUID(topic[3]))
                            self.opus_interfaces['mqtt<maestro>'].publish(
                                payload['callback'],
                                json.dumps({
                                    "device_name": device.name,
                                    "device_pk": str(device.id),
                                    "device_type": device.type,
                                })
                            )
                            return
                        except Exception as exc: # pylint: disable=broad-except
                            log.warning(msg.payload)
                            self.opus_interfaces['mqtt<maestro>'].publish(
                                payload['callback'],
                                json.dumps({
                                    'status': 'failed',
                                    'reason': str(exc)
                                })
                            )
                            return
                    case 'get_state':
                        try:
                            temp = json.loads(msg.payload)
                            device = self.get_device(UUID(topic[3]))
                            self.opus_interfaces['mqtt<maestro>'].publish(
                                payload['callback'],
                                json.dumps(device.get_state())
                            )
                            return
                        except Exception as exc: # pylint: disable=broad-except
                            log.warning(msg.payload)
                            self.opus_interfaces['mqtt<maestro>'].publish(
                                payload['callback'],
                                json.dumps({
                                    'status': 'failed',
                                    'reason': str(exc)
                                })
                            )
                            self.opus_interfaces['mqtt<local>'].publish(
                                payload['callback'],
                                json.dumps({
                                    'status': 'failed',
                                    'reason': str(exc)
                                })
                            )
                            return
                    case 'set_state':
                        try:
                            temp = json.loads(msg.payload)
                            user: models.User = self.users_managers.get_user(temp['user_id'])
                            device = self.get_device(UUID(topic[3]))
                            if user is None:
                                user = models.User()
                                user.user_pk = None
                                user.given_name = temp['user']['given_name']
                                user.email = temp['user']['email']
                            try:
                                db_session = next(self.opus_db.get_db())
                                role: models.Role = crud.get_role_uuid(db_session, user.fk_role)
                                if role is None:
                                    role = crud.get_role_by_name(db_session, 'Guest')
                            except AttributeError as exc:
                                role = crud.get_role_by_name(db_session, 'Guest')
                            finally:
                                db_session.close()                                
                            if role.role_name == 'Guest':
                                if not self.users_managers.check_if_device_accepts_guests(device):
                                    log.warning(f'{user.given_name} is a guest and device {device.name} does not accept guests')
                                    # raise ValueError('Device does not accept guests')
                                    return
                            else:
                                if not self.users_managers.check_user_access_to_device(user, device):
                                    log.warning(f'{user.given_name} does not have access to device {device.name}')
                                    # raise ValueError(f'{user.given_name} does not have access to this device')
                                    return
                            log.info(f"User {user.given_name} [{role.role_name}] is accessing device {device.name}")
                            device.set_state(temp['state'])
                            self.opus_interfaces['mqtt<maestro>'].publish(
                                payload['callback'],
                                json.dumps({'status': 'success'})
                            )
                            self.opus_interfaces['mqtt<local>'].publish(
                                payload['callback'],
                                json.dumps({'status': 'success'})
                            )
                            return
                        except Exception as exc: # pylint: disable=broad-except
                            log.error("Exception: %s", exc)
                            log.error("Traceback:\n%s", traceback.format_exc())
                            self.opus_interfaces['mqtt<maestro>'].publish(
                                payload['callback'],
                                json.dumps({
                                    'status': 'failed',
                                    'reason': str(exc)
                                })
                            )
                    case 'get_type':
                        try:
                            temp = json.loads(msg.payload)
                            device = self.get_device(UUID(topic[3]))
                            self.opus_interfaces['mqtt<maestro>'].publish(
                                payload['callback'],
                                json.dumps({'type': device.type})
                            )
                            return
                        except Exception as exc: # pylint: disable=broad-except
                            log.warning(msg.payload)
                            self.opus_interfaces['mqtt<maestro>'].publish(
                                payload['callback'],
                                json.dumps({
                                    'status': 'failed',
                                    'reason': str(exc)
                                })
                            )
                if topic[2] in self.opus_drivers:
                    try:
                        log.debug("Driver specific message received, sending to %s.", topic[2])
                        self.opus_drivers[topic[2]]._mqtt_callback(topic, json.loads(msg.payload)) # pylint: disable=protected-access
                        self.opus_interfaces['mqtt<local>'].publish(
                                payload['callback'],
                                json.dumps({'status': 'success'})
                            )
                        self.opus_interfaces['mqtt<maestro>'].publish(
                            payload['callback'],
                            json.dumps({'status': 'success'})
                        )
                    except json.JSONDecodeError:
                        log.error('Invalid JSON Received')
                        self.opus_interfaces['mqtt<local>'].publish(
                                payload['callback'],
                                json.dumps({
                                    'status': 'failed',
                                    'reason': 'Invalid JSON Received'
                                    })
                            )
                        self.opus_interfaces['mqtt<maestro>'].publish(
                            payload['callback'],
                            json.dumps({
                                'status': 'failed',
                                'reason': 'Invalid JSON Received'
                                })
                        )
                else:
                    try:
                        device_id = UUID(topic[2])
                        device = self.get_device(device_id)
                        self._device_command(device, payload)
                    except ValueError:
                        log.error('Invalid Command Received')
                        self.opus_interfaces['mqtt<local>'].publish(
                                payload['callback'],
                                json.dumps({
                                    'status': 'failed',
                                    'reason': 'Invalid Command Received'
                                    })
                            )
                        self.opus_interfaces['mqtt<maestro>'].publish(
                            payload['callback'],
                            json.dumps({
                                'status': 'failed',
                                'reason': 'Invalid Command Received'
                                })
                        )
            case _:
                log.error('Invalid Topic Received')
                self.opus_interfaces['mqtt<local>'].publish(
                        payload['callback'],
                        json.dumps({
                            'status': 'failed',
                            'reason': 'Invalid Topic Received'
                            })
                    )

    def _device_command(self, device, command: json) -> None:
        """Receive a command from MQTT"""
        log.debug('Device Command Received')
        log.debug('├── Device ID: %s', device.id)
        log.debug('└──> Command: %s', command)
        match device.type:
            case 'LIGHT':
                match command['cmnd']:
                    case "on":
                        device.on()
                    case "off":
                        device.off()
                    case "toggle":
                        device.toggle()
            case 'HVAC':
                match command['cmnd']:
                    case "on":
                        device.on()
                    case "off":
                        device.off()
                    case "set_temperature":
                        device.set_temperature(command['temperature'])
                    case "set_mode":
                        device.set_mode(command['mode'])
                    case "set_fan_speed":
                        device.set_fan_speed(command['fan_speed'])
            case _:
                log.error('Device Type not found')
