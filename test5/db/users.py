"""Users handler for the database"""
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from db.models import OpusUser

def get_user_by_google_sub(db: Session, google_sub: str) -> OpusUser:
    """Get a user by google sub"""
    return db.query(OpusUser).filter(OpusUser.google_sub == google_sub).first()

def create_user(db: Session, user: OpusUser) -> OpusUser:
    """Create a user"""
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f'User created: {user.email}')
    return user

def get_user_by_id(db: Session, user_id: str) -> OpusUser:
    """Get a user by id"""
    return db.query(OpusUser).filter(OpusUser.user_id == user_id).first()

def get_user_by_email(db: Session, email: str) -> OpusUser:
    """Get a user by email"""
    return db.query(OpusUser).filter(OpusUser.email == email).first()

def get_all_users(db: Session):
    """Get all users"""
    return db.query(OpusUser).all()

def get_servers_of_user(db: Session, user_id: str):
    """Get all server which a User is registered on"""
    temp = db.execute(text(f"SELECT server_id FROM roles WHERE user_id = \'{user_id}\'")).all()
    server_list = []
    for server in temp:
        server_list.append((str(server[0])))
    return server_list

def get_servers_of_user_by_google_sub(db: Session, google_sub: str):
    """Get all server which a User is registered on"""
    user = get_user_by_google_sub(db, google_sub)
    if user:
        return get_servers_of_user(db, str(user.user_id))
    return []

def delete_user(db: Session, user: OpusUser):
    """Delete a user"""
    db.delete(user)
    db.commit()
    return user
