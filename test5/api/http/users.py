"""HTTP API Users Endpoints"""
from fastapi import APIRouter, status, Response
from fastapi.responses import HTMLResponse
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request
from db.models import OpusUser
import db.users as opus_users
import db.localservers as opus_servers
from db.database import DB
from configurations.config import OpenConfig
from api.http.models import Role

config = OpenConfig()
db = DB(config["database"]["url"])

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.get("/")
async def get_all_users():
    """Users endpoint for the server."""
    return opus_users.get_all_users(next(db.get_db()))

@router.delete("/delete/{user_id}")
async def delete_user(user_id: str):
    """Delete user endpoint for the server."""
    db_session = next(db.get_db())
    user = opus_users.get_user_by_id(db_session, user_id)
    if user:
        return opus_users.delete_user(db_session, user)
    return "User not found", status.HTTP_404_NOT_FOUND

@router.post("/set_role")
async def set_user_role(role: Role):
    """Set user role endpoint for the server."""
    db_session = next(db.get_db())
    return opus_servers.set_user_server_role(
        db_session,
        role.user_id,
        role.server_id,
        role.role
    )

@router.get("/server/{user_id}")
async def get_user_servers(user_id: str):
    """Get user servers endpoint for the server."""
    db_session = next(db.get_db())
    return opus_users.get_servers_of_user(db_session, user_id)
