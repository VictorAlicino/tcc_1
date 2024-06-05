"""Local Servers handler for the database"""
from sqlalchemy.orm import Session
from db.models import OpusServer

def create_server(db: Session, server: OpusServer) -> OpusServer:
    """Create a server"""
    db.add(server)
    db.commit()
    db.refresh(server)
    print(f'Server created: {server.name}')
    return server