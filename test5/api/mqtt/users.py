"""MQTT API endpoints for the users comms'."""
import json
import aiomqtt
import asyncio
import logging
from sqlalchemy.orm import Session
import db.localservers as opus_servers
import db.users as maestro_users
from db.models import OpusServer, MaestroUser
from db.database import DB
from decouple import config as env
from api.mqtt.basic_comms import send_msg_to_server, receive_callback

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

async def dump_all_info_from_a_user(local_server: OpusServer, user: MaestroUser) -> json:
    """Dump all info from a user."""
    data: dict = {
        "user_pk": str(user.user_id),
        "callback": env('CLOUD-MQTT') + "/users/get_user_full/callback"
    }

    send_task = asyncio.create_task(send_msg_to_server(local_server, "cloud/get_user_full", data))
    receive_task = asyncio.create_task(receive_callback(env('CLOUD-MQTT') + "/users/get_user_full/callback"))

    await send_task
    result: json = await receive_task
    if (result):
        result['buildings'] = [
            {**building, "server_pk": local_server.server_id} for building in result['buildings']
        ]

    return result
