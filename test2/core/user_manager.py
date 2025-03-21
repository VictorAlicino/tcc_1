"""User manager to handle permissions"""
import logging
import json
import uuid
from datetime import datetime
from hashlib import sha3_256
from sqlalchemy.orm import Session
from sqlalchemy import select, func, text, UUID
import db.crud as crud
from db.models import User
from db.models import Device

log = logging.getLogger(__name__)

class UserManager:
    """User manager to handle permissions"""
    def __init__(self,
                 dirs: dict,
                 interfaces: dict,
                 managers: dict,
                 drivers: dict
                ):
        log.debug('Initializing User Manager.')
        self.opus_db = interfaces['opus_db']
        self.dirs = dirs
        self.interfaces = interfaces
        self.managers = managers
        self.drivers = drivers

        log.info("Check in for updates on database, this may take a while...")
        self.db_hash: str = self._generate_db_hash()
        log.info("Database up to date!")
        self._mqtt_root_topic = ""
        self._configure_mqtt()
        log.info('User Manager initialized.')

    def _generate_db_hash(self) -> str:
        """Generates a DB Hash according to specification"""
        hash = sha3_256(str(datetime.timestamp(datetime.now())).encode('utf-8'))
        return hash

    def _configure_mqtt(self) -> None:
        """Configure MQTT"""
        log.debug('Configuring MQTT for Users Manager.')
        self.interfaces['mqtt<maestro>'].register_callback('users/#', self._mqtt_callback)
        self._mqtt_root_topic = f'{self.interfaces["mqtt<maestro>"].client_id}/users'
        log.debug('MQTT Configured for Users Manager.')

    def _mqtt_callback(self, client, userdata, msg): # pylint: disable=unused-argument
        """Callback from MQTT when Maestro sends a message in the /users topic"""
        match msg.topic:
            case topic if topic == f'{self._mqtt_root_topic}/add':
                self._assign_maestro_user(json.loads(msg.payload))
            case _:
                print("Message not recognized by the User Manager")

    def _assign_maestro_user(self, maestro_user: json) -> User | None:
        """Assign to this server a user coming from Maestro"""
        user: User = User()
        user_pk, user_data = next(iter(maestro_user.items()))
        # Checking if User already existis in DB
        db = next(self.opus_db.get_db())
        try:
            if crud.get_user_by_id(db, user_pk):
                log.warn('User %s already on this server', user_data['name'])
                return None
            user.user_pk = uuid.UUID(user_pk)
            user.given_name = user_data['name']
            user.email = user_data['email']
            role = crud.get_role_by_id(db, user_data['role'])
            if not role:
                log.warn('Role requested by Maestro does not exist')
                return None
            user.fk_role = role.role_pk
            crud.assign_new_user(db, user)
            log.debug('User %s added to the database with role %s', user.given_name, role.role_name)
        finally:
            db.close()

    def check_user_access_to_device(self, user: User, device: Device) -> bool:
        """Check if a user has access to a device"""
        if not user:
            log.error('User does not exist')
            return False
        if not device:
            log.error('Device does not exist')
            return False
        db = next(self.opus_db.get_db())
        try:
            user_role = crud.get_role_uuid(db, user.fk_role)
            if device.id in [device.device_pk for device in crud.get_all_devices_authorized_to_a_role(db, user_role)]:
                return True
            return False
        finally:
            db.close()

    def check_if_device_accepts_guests(self, device: Device) -> bool:
        """Check if a device accepts guests"""
        db = next(self.opus_db.get_db())
        try:
            if device.id in [device.device_pk for device in crud.get_all_devices_authorized_to_a_role(db, crud.get_role_by_name(db, 'Guest'))]:
                return True
            return False
        finally:
            db.close()
    
    def get_user(self, user_pk: str) -> User:
        """Get a user by its PK"""
        db = next(self.opus_db.get_db())
        try:
            return crud.get_user_by_id(db, user_pk)
        finally:
            db.close()