"""Database ORM"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base
from configurations.singleton_metaclass import SingletonMeta
import logging

# Logger
log = logging.getLogger(__name__)

class DB(metaclass=SingletonMeta):
    """Database ORM"""
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.session_local = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_db(self):
        """Get the database session"""
        db = self.session_local()
        try:
            yield db
        finally:
            db.close()

    def create_all(self):
        """Create all tables"""
        log.info("Creating tables if they don't already exists")
        Base.metadata.create_all(bind=self.engine)
