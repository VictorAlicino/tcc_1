"""HTTP API Local Servers (Opus) Endpoints"""
import logging
import json
from fastapi import APIRouter, status, Response
from fastapi.responses import JSONResponse
from sqlalchemy.dialects.postgresql import UUID
from fastapi.responses import HTMLResponse
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request
from db.models import MaestroUser
import db.users as maestro_users
import db.localservers as opus_servers
from db.database import DB
from db.models import OpusServer
from configurations.config import OpenConfig
from api.rest._api_models import UserRole
import api.mqtt.users as MQTT_Users

log = logging.getLogger(__name__)
config = OpenConfig()
db = DB()

router = APIRouter(
    prefix="/opus_server",
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
            user = maestro_users.get_user_by_id(db_session, row.user_id)
            admins.append((user.user_id, user.email))
        return {
            "server_id": server_id,
            "admins": admins
        }
    return "Server not found", status.HTTP_404_NOT_FOUND

@router.post("/assign_users/{server_id}")
async def assign_users_to_server(server_id: str, server_user_list: list[UserRole]):
    """Assign a new server to a list of users"""
    db_session = next(db.get_db())
    local_server: OpusServer | None = opus_servers.get_server_by_id(db_session, server_id)
    if not local_server:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content="Server not found"
        )
    report: list = []
    entries: list[tuple] = []
    error_flag: bool = False
    for entry in server_user_list:
        # Check in the db if users even exists in Maestro
        user: MaestroUser | None = maestro_users.get_user_by_id(db_session, entry.user_id)
        if user is None:
            log.warn('BAD REQUEST -> User %s cannot be assigned to server %s - not available', 
                    entry.user_id, local_server.name)
            report.append({entry.user_id: status.HTTP_400_BAD_REQUEST})
            error_flag = True
            continue
        entries.append((user, entry.role))
        report.append({entry.user_id: status.HTTP_201_CREATED})
    await MQTT_Users.register_new_user(local_server, entries)
    if error_flag is True:
        return JSONResponse(
            content=report,
            status_code=status.HTTP_207_MULTI_STATUS
        )
    else:
        return JSONResponse(
            content=report,
            status_code=status.HTTP_201_CREATED
        )

@router.get("/users/{server_id}")
async def get_server_users(server_id: str):
    """Get server users endpoint for the server."""
    db_session = next(db.get_db())
    result =  opus_servers.get_server_users(db_session, server_id)
    if result:
        users = []
        for row in result:
            user = maestro_users.get_user_by_id(db_session, row.user_id)
            users.append((user.user_id, user.email))
        return {
            "server_id": server_id,
            "users": users
        }
    return "Server not found", status.HTTP_404_NOT_FOUND

@router.get("/user/devices")
async def get_user_devices(server_id: str):
    """Get all user devices from the server provided."""
    # This will only work with the user on the provided JWT Token
    # The user will be the one that is logged in
    # TODO: Implement this

@router.post("/cmd/{server_id}")
async def command(server_id: str, cmd: dict):
    """Command endpoint for the server."""
    send_cmd_to_server(server_id, cmd)
    return "Command sent", status.HTTP_200_OK
