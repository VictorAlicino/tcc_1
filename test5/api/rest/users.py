"""HTTP API Users Endpoints"""
import json
from fastapi import APIRouter, status, Response, Depends
from fastapi.responses import HTMLResponse
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request
from jose import JWTError, jwt

from db.models import MaestroUser, OpusServer
import db.users as maestro_users
import db.localservers as opus_servers
from db.database import DB
from configurations.config import CONFIG
from api.rest.auth_conductor import oauth2_scheme
from api.mqtt.users import dump_all_info_from_a_user

db = DB()

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.get("/")
async def get_all_users():
    """Users endpoint for the server."""
    return maestro_users.get_all_users(next(db.get_db()))

@router.delete("/delete/{user_id}")
async def delete_user(user_id: str):
    """Delete user endpoint for the server."""
    db_session = next(db.get_db())
    user = maestro_users.get_user_by_id(db_session, user_id)
    if user:
        return maestro_users.delete_user(db_session, user)
    return "User not found", status.HTTP_404_NOT_FOUND

@router.get("/server/{user_id}")
async def get_user_servers(user_id: str):
    """Get user servers endpoint for the server."""
    db_session = next(db.get_db())
    return maestro_users.get_servers_of_user(db_session, user_id)

@router.post("/opus_server/dump_all_servers_info")
async def dump_all_servers_info(request: Request, validate: str = Depends(oauth2_scheme)):
    """Dump all servers info endpoint for the server."""
    token_decoded: dict = jwt.decode(validate, CONFIG['api-secrets']['secret_key'], algorithms=["HS256"])
    db_session = next(db.get_db())
    user_servers: list[MaestroUser, list[OpusServer]] =  maestro_users.get_servers_of_user_by_google_sub(db_session, token_decoded['sub'])
    servers_dumped: dict = {}
    
    for server in user_servers[1]:
        servers_dumped[server.name] = await dump_all_info_from_a_user(server, user_servers[0])

    return servers_dumped
