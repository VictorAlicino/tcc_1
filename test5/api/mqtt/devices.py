"""MQTT API endpoints for the devices comms'."""
import json
import aiomqtt
import asyncio
import uuid
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

async def get_device(local_server: OpusServer, device_id: str) -> json:
    """Get a device from the server."""
    request_id = str(uuid.uuid4())
    data: dict = {
        "device_id": device_id,
        "callback": env('CLOUD-MQTT') + "/devices/get_device/callback/" + request_id
    }

    send_task = asyncio.create_task(send_msg_to_server(local_server, f"devices/get/{device_id}", data))
    receive_task = asyncio.create_task(receive_callback(env('CLOUD-MQTT') + f"/devices/get_device/callback/{request_id}"))

    await send_task
    result = await receive_task

    return result

async def get_device_state(local_server: OpusServer, device_id: str) -> json:
    """Get the state of a device."""
    request_id = str(uuid.uuid4())
    data: dict = {
        "device_id": device_id,
        "callback": env('CLOUD-MQTT') + "/devices/get_device_state/callback/" + request_id
    }

    send_task = asyncio.create_task(send_msg_to_server(local_server, f"devices/get_state/{device_id}", data))
    receive_task = asyncio.create_task(receive_callback(env('CLOUD-MQTT') + f"/devices/get_device_state/callback/{request_id}"))

    await send_task
    result = await receive_task

    return result

async def device_set_state(local_server: OpusServer, user: MaestroUser, device_id: str, state: json) -> json:
    """Set the state of a device."""
    request_id = str(uuid.uuid4())
    data: dict = {
        "device_id": device_id,
        "user_id": str(user.user_id),
        "state": state,
        "callback": env('CLOUD-MQTT') + "/devices/set_device_state/callback/" + request_id
    }

    send_task = asyncio.create_task(send_msg_to_server(local_server, f"devices/set_state/{device_id}", data))
    receive_task = asyncio.create_task(receive_callback(env('CLOUD-MQTT') + f"/devices/set_device_state/callback/{request_id}"))

    await send_task
    result = await receive_task

    return result

async def get_device_type(local_server: OpusServer, device_id: str) -> json:
    """Get the type of a device."""
    request_id = str(uuid.uuid4())
    data: dict = {
        "device_id": device_id,
        "callback": env('CLOUD-MQTT') + "/devices/get_device_type/callback/" + request_id
    }

    send_task = asyncio.create_task(send_msg_to_server(local_server, f"devices/get_type/{device_id}", data))
    receive_task = asyncio.create_task(receive_callback(env('CLOUD-MQTT') + f"/devices/get_device_type/callback/{request_id}"))

    await send_task
    result = await receive_task

    return result
