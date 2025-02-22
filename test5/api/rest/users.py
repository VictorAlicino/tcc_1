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

def _decode_jwt(token: str):
    try:
        return jwt.decode(token, CONFIG['api-secrets']['secret_key'], algorithms=["HS256"])
    except JWTError:
        return None
    
def get_user_requesting(token: str, db_session):
    token_decoded = _decode_jwt(token)
    if token_decoded:
        return maestro_users.get_user_by_google_sub(db_session, token_decoded['sub'])
    return None

@router.get("/")
async def get_all_users():
    """Endpoint to get all users from the server."""
    users = None
    with db.get_db() as db_session:
        users = maestro_users.get_all_users(db_session)
    return users

@router.get("/{user_id}")
async def get_user(user_id: str):
    """Endpoint to get a user from the server."""
    user = None
    with db.get_db() as db_session:
        user = maestro_users.get_user_by_id(db_session, user_id)
    return user

@router.delete("/{user_id}/delete")
async def delete_user(user_id: str):
    """Endpoint to delete a user from the server."""
    user: MaestroUser = None
    with db.get_db() as db_session:
        user = maestro_users.get_user_by_id(db_session, user_id)
    if user:
        with db.get_db() as db_session:
            maestro_users.delete_user(db_session, user)
        return "User deleted", status.HTTP_200_OK
    return "User not found", status.HTTP_404_NOT_FOUND

@router.get("/{user_id}/servers")
async def get_user_servers(user_id: str):
    """Endpoint to get all servers of a user."""
    with db.get_db() as db_session:
        return maestro_users.get_servers_of_user(db_session, user_id)

@router.get("/opus_server/dump")
async def dump_all_servers_info(validate: str = Depends(oauth2_scheme), db_session=Depends(db.get_db)):
    """Dump all servers info endpoint for the server."""
    token_decoded: dict = jwt.decode(validate, CONFIG['api-secrets']['secret_key'], algorithms=["HS256"])
    user_servers: list[MaestroUser, list[OpusServer]] = maestro_users.get_servers_of_user_by_google_sub(db_session, token_decoded['sub'])
    servers_dumped: list = []

    for server in user_servers[1]:
        server_response: json = await dump_all_info_from_a_user(server, user_servers[0])
        if server_response:
            for building in server_response['buildings']:
                servers_dumped.append(building)

    return servers_dumped
