"""User manager to handle permissions"""
import logging
import json
from datetime import datetime
from hashlib import sha3_256
from sqlalchemy.orm import Session
from sqlalchemy import select, func, text
from db.models import User

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
        log.debug('MQTT Configured for Users Manager.')

    def _mqtt_callback(self, client, userdata, msg): # pylint: disable=unused-argument
        """Callback from MQTT when Maestro sends a message in the /users topic"""
        match msg.topic:
            case topic if topic == f'{self.interfaces['mqtt<maestro>'].client_id}/users/add':
                print(f'User received from Maestro:\n{json.loads(msg.payload)}')
            case _:
                print("Message not recognized by the User Manager")
