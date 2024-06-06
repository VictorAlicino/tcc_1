"""Database ORM"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base

class SingletonMeta(type):
    """Singleton metaclass"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class DB(metaclass=SingletonMeta):
    """Database ORM"""
    def __init__(self, db_url: str):
        print("Loading database")
        self.engine = create_engine(db_url)
        self.session_local = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        print("Database loaded")

    def get_db(self):
        """Get the database session"""
        db = self.session_local()
        try:
            yield db
        finally:
            db.close()

    def create_all(self):
        """Create all tables"""
        print("Creating tables if they don't already exists")
        Base.metadata.create_all(bind=self.engine)
