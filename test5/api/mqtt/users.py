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

async def register_new_user(local_server: OpusServer, user: MaestroUser) -> None:
    """Register an Maestro User into the Local Server"""
    log.debug("Registering %s into %s", user.given_name, local_server.name)
    print("enviando uma batatinha pro servidor local")
    await send_msg_to_server(local_server, "receitas/batatas", {"BATATINHA_FRITA": "123"})
