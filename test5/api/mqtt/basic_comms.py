"""MQTT API endpoints for the server."""
import json
import aiomqtt
import logging
import asyncio
import db.localservers as opus_servers
import db.users as maestro_users
from db.models import OpusServer
from db.database import DB
from decouple import config as env

# Logger
log = logging.getLogger(__name__)
db = DB()

async def check_if_server_exists(server_name: str) -> OpusServer | bool:
    """Check if a server exists."""
    server = opus_servers.get_server_by_name(next(db.get_db()), server_name)
    if server:
        return server
    return False

async def send_msg_to_server(local_server: OpusServer, topic:str, command: dict):
    """Send a command to a server."""
    full_topic = local_server.mqtt_topic[:-1] + topic
    #log.debug("Publishing to %s the following message:\n%s", full_topic, json.dumps(command))
    async with aiomqtt.Client(env('CLOUD-MQTT')) as client:
        await client.publish(full_topic, json.dumps(command))

async def receive_callback(callback_topic: str, timeout: float = 0.5) -> json:
    """Receive a callback from a server with a timeout."""
    async with aiomqtt.Client(env('CLOUD-MQTT')) as client:
        await client.subscribe(callback_topic)

        async def wait_for_message():
            async for message in client.messages:
                return json.loads(message.payload.decode())
        try:
            return await asyncio.wait_for(wait_for_message(), timeout)
        except asyncio.TimeoutError:
            return None

async def server_login_listener():
    """Receives Login requests from new servers."""
    log.info("Listening on mqtt (maestro/login) for new servers.")
    async with aiomqtt.Client(env('CLOUD-MQTT')) as client:
        await client.subscribe("maestro/login")
        while True: # Change this for a more deterministic way to stop the listener
            async for message in client.messages:
                message_temp = json.loads(message.payload.decode())
                log.debug("New server login request received.")
                server = await check_if_server_exists(message_temp['client_id'])
                if server is False:
                    log.info("New server requested to connect to Maestro.")
                    new_server = opus_servers.create_server(
                        next(db.get_db()),
                        OpusServer(
                            name= message_temp['client_id'],
                            ip_address= message_temp['ip_address'],
                            mqtt_topic= message_temp['mqtt_topic'],
                        )
                    )
                    await client.publish(
                        message_temp['callback'],
                        json.dumps(
                            {
                                "status": "success",
                                "message": "Server created",
                                "payload": {
                                    "server_name": f"{new_server.name}",
                                    "server_id": f"{new_server.server_id}"
                                }
                            }
                        )
                    )
                    server = new_server;
                    log.info(f"{server.name} registered and connected to Maestro.")
                else:
                    await client.publish(
                    message_temp['callback'],
                    json.dumps({"status": "success"})
                    )
                    log.info(f"{server.name} connected to Maestro.")
