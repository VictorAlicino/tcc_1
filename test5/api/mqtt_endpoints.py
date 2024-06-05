"""MQTT API endpoints for the server."""
import aiomqtt
import yaml
import json
from db.localservers import create_server
from db.models import OpusServer
from db.database import DB

# Load YAML file
with open("config.yaml", "r", encoding='utf-8') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

db = DB(config["database"]["url"])

async def server_login_listener():
    """Receives Login requests from new servers."""
    async with aiomqtt.Client("168.75.84.130") as client:
        await client.subscribe("maestro/login")
        while True: # Change this for a more deterministic way to stop the listener
            async for message in client.messages:
                message_temp = json.loads(message.payload.decode())
                #print(f"Received message: {message_temp}")
                # Create a new server
                new_server = create_server(
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
                    ))
