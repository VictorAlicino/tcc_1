"""User manager to handle permissions"""
import logging

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
        self.dirs = dirs
        self.interfaces = interfaces
        self.managers = managers
        self.drivers = drivers
        self.load_users()
        log.info('User Manager initialized.')

    def load_users(self):
        """Load users from database"""
        log.debug('Loading users from database.')
        self.users = {}
