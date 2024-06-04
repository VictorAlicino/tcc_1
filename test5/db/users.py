"""Users handler for the database"""
from sqlalchemy.orm import Session
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

def delete_user(db: Session, user: OpusUser):
    """Delete a user"""
    db.delete(user)
    db.commit()
    return user

def change_user_role(db: Session, user: OpusUser, role: int):
    """Change a user's role"""
    user.role = role
    db.commit()
    db.refresh(user)
    return user
