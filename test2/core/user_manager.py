"""User manager to handle permissions"""
import logging
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
        
        #self.db_checksum: str = self._generate_db_checksum()
        log.info('User Manager initialized.')

    def _generate_db_checksum(self) -> str:
        """Reads the user database and generate a checksum"""
        log.info("Check in for updates on database, this may take a while...")
        db: Session = next(self.opus_db.get_db())
        columns = ', '.join(
            [f"COALESCE(CAST({column.name} AS CHAR), '')" for column in User.__table__.columns]
            )
        print(columns)
        query = select(
            [func.md5(
                func.group_concat(
                    text(
                        f"CONCAT_WS(',', {columns}) ORDER BY id"
                        )
                    )
                )
            ]).select_from(User.__table__)
        result = db.execute(query)
        print(result)
        log.info("Database up to date!")
        return result