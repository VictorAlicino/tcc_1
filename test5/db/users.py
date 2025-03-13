"""Users handler for the database"""
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from db.models import MaestroUser, OpusServer

def get_user_by_google_sub(db: Session, google_sub: str) -> MaestroUser | None:
    """Get a user by google sub"""
    return db.query(MaestroUser).filter(MaestroUser.google_sub == google_sub).first()

def create_user(db: Session, user: MaestroUser) -> MaestroUser | None:
    """Create a user"""
    db.add(user)
    db.commit()
    db.refresh(user)
    #print(f'User created: {user.email}')
    return user

def get_user_by_id(db: Session, user_id: str) -> MaestroUser | None:
    """Get a user by id"""
    return db.query(MaestroUser).filter(MaestroUser.user_id == user_id).first()

def get_user_by_email(db: Session, email: str) -> MaestroUser | None:
    """Get a user by email"""
    return db.query(MaestroUser).filter(MaestroUser.email == email).first()

def get_all_users(db: Session):
    """Get all users"""
    return db.query(MaestroUser).all()

def get_servers_of_user(db: Session, user_id: str):
    """Get all server which a User is registered on"""
    temp = db.execute(text(f"SELECT DISTINCT server_id FROM roles WHERE user_id = \'{user_id}\'")).all()
    server_list = []
    for server in temp:
        server_list.append((str(server[0])))
    return server_list

def get_servers_of_user_by_google_sub(db: Session, google_sub: str) -> list[MaestroUser, list[OpusServer]]:
    """Get all server which a User is registered on"""
    user = get_user_by_google_sub(db, google_sub)
    server_list: list[OpusServer] = []
    if user:
        severs = get_servers_of_user(db, str(user.user_id))
        server_list = db.query(OpusServer).filter(OpusServer.server_id.in_(severs)).all()
    return [user, server_list]

def delete_user(db: Session, user: MaestroUser):
    """Delete a user"""
    db.delete(user)
    db.commit()
    return user
