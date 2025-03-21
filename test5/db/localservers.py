"""Local Servers handler for the database"""
from sqlalchemy.orm import Session
from db.models import OpusServer, roles
from db.models import MaestroUser
from sqlalchemy.dialects.postgresql import UUID

def create_server(db: Session, server: OpusServer) -> OpusServer:
    """Create a server"""
    db.add(server)
    db.commit()
    db.refresh(server)
    return server

def get_server_by_id(db: Session, server_id: str) -> OpusServer | None:
    """Get a server by id"""
    return db.query(OpusServer).filter(OpusServer.server_id == server_id).first()

def get_server_by_name(db: Session, name: str) -> OpusServer:
    """Get a server by name"""
    return db.query(OpusServer).filter(OpusServer.name == name).first()

def get_all_servers(db: Session):
    """Get all servers"""
    return db.query(OpusServer).all()

def delete_server(db: Session, server: OpusServer):
    """Delete a server"""
    db.delete(server)
    db.commit()
    return server

def set_user_server_role(db: Session, user_id: str, server_id: str, role: int):
    """Set a Role for a User in that Server"""
    db.execute(
        roles.insert().values(
            user_id=user_id,
            server_id=server_id,
            role=role
        )
    )
    db.commit()
    return f"User {user_id} has been set as {role} in server {server_id}"

def get_server_admins(db: Session, server_id: str):
    """Get all admins in a server"""
    # Admins are role 0
    return db.query(roles.c.user_id).filter(roles.c.server_id == server_id, roles.c.role == 0).all()

def assign_users_to_server(db: Session, server_id: str, users: list[tuple[MaestroUser, int]],):
    """Assign users to a server"""
    for user in users:
        db.execute(
            roles.insert().values(
                user_id=str(user[0].user_id),
                server_id=str(server_id),
                role=user[1]
            )
        )
    db.commit()
    return f"Users have been assigned to server {server_id}"

def get_server_users(db: Session, server_id: str):
    """Get all users in a server"""
    return db.query(roles).filter(roles.c.server_id == server_id).all()
