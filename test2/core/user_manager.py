"""User manager to handle permissions"""
import logging
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
        log.info('User Manager initialized.')

    def _generate_db_hash(self) -> str:
        """Generates a DB Hash according to specification"""
        hash = sha3_256(str(datetime.timestamp(datetime.now())).encode('utf-8'))
        return hash