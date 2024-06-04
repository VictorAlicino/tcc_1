"""Database ORM"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from db.models import Base


class DB:
    """Database ORM"""
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url, connect_args={"check_same_thread": False})
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
        Base.metadata.create_all(bind=self.engine)

