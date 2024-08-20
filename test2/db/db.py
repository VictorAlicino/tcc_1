"""Database configuration and session management"""
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from db import models

log = logging.getLogger(__name__)

Base = declarative_base()

class OpusDB:
    """Database Class"""
    def __init__(self, db_dir: str):
        log.debug('Starting Database')
        self.engine = create_engine(
            f'sqlite:///{db_dir}/opus-vault.db',
            connect_args={"check_same_thread": False}
            )
        self.session_local = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        models.Base.metadata.create_all(bind=self.engine)
        log.info('Database Started')

    def get_db(self):
        """Get database session"""
        db: Session = self.session_local()
        try:
            yield db
        finally:
            db.close()
