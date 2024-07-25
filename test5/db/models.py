"""Models for the ORM"""
import uuid
from sqlalchemy import Column, String, ForeignKey, Table, SmallInteger
from sqlalchemy.dialects.postgresql import UUID, BYTEA
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# User Model
class MaestroUser(Base):
    """User model."""
    __tablename__ = 'maestro_user'

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String)
    name = Column(String)
    given_name = Column(String)
    family_name = Column(String)
    google_sub = Column(String)
    picture_url = Column(String)
    picture = Column(BYTEA)

# Local Server (Opus) Model
class OpusServer(Base):
    """Opus Server model."""
    __tablename__ = 'opus_server'

    server_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    ip_address = Column(String)
    mqtt_topic = Column(String)

# N to N Relationship to define users roles
roles = Table('roles',
              Base.metadata,
              Column('user_id', UUID, ForeignKey('maestro_user.user_id')),
              Column('server_id', UUID, ForeignKey('opus_server.server_id')),
              Column('role', SmallInteger, default=1) # 0 = Admin, 1 = User
             )
