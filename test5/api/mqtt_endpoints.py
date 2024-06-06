"""MQTT API endpoints for the server."""
import aiomqtt
import yaml
import json
import db.localservers as opus_servers
from db.models import OpusServer
from db.database import DB

# Load YAML file
with open("config.yaml", "r", encoding='utf-8') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

db = DB(config["database"]["url"])

async def check_if_server_exists(server_name: str) -> OpusServer | bool:
    """Check if a server exists."""
    server = opus_servers.get_server_by_name(next(db.get_db()), server_name)
    if server:
        return server
    return False

async def server_login_listener():
    """Receives Login requests from new servers."""
    print("Listening on mqtt (maestro/login) for new servers.")
    async with aiomqtt.Client("168.75.84.130") as client:
        await client.subscribe("maestro/login")
        while True: # Change this for a more deterministic way to stop the listener
            async for message in client.messages:
                message_temp = json.loads(message.payload.decode())
                print("New server login request received.")
                server = await check_if_server_exists(message_temp['client_id'])
                if server is False:
                    print("New server requested to connect to Maestro.")
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
                    continue
                await client.publish(
                        message_temp['callback'],
                        json.dumps(
                            {
                                "status": "sucess",
                                "message": "Connected to Maestro",
                                "payload": {
                                    "server_name": f"{server.name}",
                                    "server_id": f"{server.server_id}"
                                }
                            }
                        )
                    )
                print(f"{server.name} connected to Maestro.")
