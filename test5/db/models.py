"""Models for the ORM"""
import uuid
from sqlalchemy import Column, String, ForeignKey, Table, SmallInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# User Model
class User(Base):
    """User model."""
    __tablename__ = 'user'

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    google_sub = Column(String)
    email = Column(String)
    name = Column(String)
    given_name = Column(String)
    family_name = Column(String)
    picture = Column(String)

# Local Server (Opus) Model
class OpusServer(Base):
    """Opus Server model."""
    __tablename__ = 'opus'

    server_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    ip_address = Column(String)
    mqtt_topic = Column(String)

# N to N Relationship to define users roles
roles = Table('roles',
              Base.metadata,
              Column('user_id', UUID, ForeignKey('user.user_id')),
              Column('server_id', UUID, ForeignKey('opus.server_id')),
              Column('role', SmallInteger, default=1)
             )
