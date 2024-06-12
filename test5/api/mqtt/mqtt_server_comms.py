"""MQTT API endpoints for the server."""
import json
import aiomqtt
import db.localservers as opus_servers
import db.users as opus_users
from db.models import OpusServer
from db.database import DB
from configurations.config import OpenConfig

# Load YAML file
config = OpenConfig()

db = DB(config["database"]["url"])

async def check_if_server_exists(server_name: str) -> OpusServer | bool:
    """Check if a server exists."""
    server = opus_servers.get_server_by_name(next(db.get_db()), server_name)
    if server:
        return server
    return False

async def send_cmd_to_server(server_id: str, command: dict):
    """Send a command to a server."""
    server = opus_servers.get_server_by_id(next(db.get_db()), server_id)
    async with aiomqtt.Client(config['cloud_mqtt']) as client:
        await client.publish(f"{server.mqtt_topic}/cmd", json.dumps(command))

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
                # If the server already exists
                # Ge the server users
                db_session = next(db.get_db())
                query = opus_servers.get_server_users(db_session, server.server_id)
                users = []
                for user in query:
                    u = opus_users.get_user_by_id(db_session, user[0])
                    users.append({
                        "user_id": f"{u.user_id}",
                        "name": f"{u.name}",
                        "email": f"{u.email}",
                        "picture": f"{u.picture}",
                        "role": int(user[2])
                    })
                await client.publish(
                        message_temp['callback'],
                        json.dumps(
                            {
                                "status": "success",
                                "message": "Connected to Maestro",
                                "payload": {
                                    "server_name": f"{server.name}",
                                    "server_id": f"{server.server_id}",
                                    "users": users
                                }
                            }
                        )
                    )
                print(f"{server.name} connected to Maestro.")
