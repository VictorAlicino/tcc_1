"""MQTT API endpoints for the users comms'."""
import json
import aiomqtt
import logging
from sqlalchemy.orm import Session
import db.localservers as opus_servers
import db.users as maestro_users
from db.models import OpusServer, MaestroUser
from db.database import DB
from decouple import config as env
from api.mqtt.basic_comms import send_msg_to_server

# Logger
log = logging.getLogger(__name__)
db = DB()

async def check_if_server_exists(server_name: str) -> OpusServer | bool:
    """Check if a server exists."""
    server = opus_servers.get_server_by_name(next(db.get_db()), server_name)
    if server:
        return server
    return False

async def register_new_user(local_server: OpusServer, entries: list[tuple[MaestroUser, int]]) -> None:
    """Register an Maestro User into the Local Server"""
    for user in entries:
        data: dict = {
            str(user[0].user_id): {
                "name": user[0].name,
                "email": user[0].email,
                "role": user[1]
            }
        }
        log.debug("Registering %s with role [%s] into %s", user[0].name, user[1], local_server.name)
        await send_msg_to_server(
            local_server,
            "users/add",
            data
            )
