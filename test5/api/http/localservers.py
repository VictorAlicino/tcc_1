"""HTTP API Local Servers (Opus) Endpoints"""
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
from api.http.models import ServerUserList

config = OpenConfig()
db = DB(config["database"]["url"])

router = APIRouter(
    prefix="/server",
    tags=["Opus Server"],
)

@router.get("/")
async def get_all_servers():
    """Servers endpoint for the server."""
    return opus_servers.get_all_servers(next(db.get_db()))

@router.delete("/delete/{server_id}")
async def delete_server(server_id: str):
    """Delete server endpoint for the server."""
    db_session = next(db.get_db())
    server = opus_servers.get_server_by_id(db_session, server_id)
    if server:
        return opus_servers.delete_server(db_session, server)
    return "Server not found", status.HTTP_404_NOT_FOUND

@router.get("/admins/{server_id}")
async def get_server_admins(server_id: str):
    """Get server admins endpoint for the server."""
    db_session = next(db.get_db())
    result =  opus_servers.get_server_admins(db_session, server_id)
    if result:
        admins = []
        for row in result:
            user = opus_users.get_user_by_id(db_session, row.user_id)
            admins.append((user.user_id, user.email))
        return {
            "server_id": server_id,
            "admins": admins
        }
    return "Server not found", status.HTTP_404_NOT_FOUND

@router.post("/assign_users")
async def assign_users_to_server(server_user_list: ServerUserList):
    """Assign users to server endpoint for the server."""
    db_session = next(db.get_db())
    return opus_servers.assign_users_to_server(
        db_session,
        server_user_list.server_id,
        server_user_list.users
    )

@router.get("/users/{server_id}")
async def get_server_users(server_id: str):
    """Get server users endpoint for the server."""
    db_session = next(db.get_db())
    result =  opus_servers.get_server_users(db_session, server_id)
    if result:
        users = []
        for row in result:
            user = opus_users.get_user_by_id(db_session, row.user_id)
            users.append((user.user_id, user.email))
        return {
            "server_id": server_id,
            "users": users
        }
    return "Server not found", status.HTTP_404_NOT_FOUND

@router.post("/cmd/{server_id}")
async def command(server_id: str, cmd: dict):
    """Command endpoint for the server."""
    send_cmd_to_server(server_id, cmd)
    return "Command sent", status.HTTP_200_OK
