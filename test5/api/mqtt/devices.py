"""MQTT API endpoints for the devices comms'."""
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

# TODO: Terminar esta
async def get_device_state(local_server: OpusServer, device_id: str) -> json:
    """Get the state of a device."""
    data: dict = {
        "device_id": device_id,
        "callback": env('CLOUD-MQTT') + "/devices/get_device_state/callback"
    }

    send_task = asyncio.create_task(send_msg_to_server(local_server, "cloud/get_device_state", data))
    receive_task = asyncio.create_task(receive_callback(env('CLOUD-MQTT') + "/devices/get_device_state/callback"))

    await send_task
    result = await receive_task

    return result