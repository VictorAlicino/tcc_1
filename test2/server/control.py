import aiotmqtt
import yaml

async def start():
    local_mqtt_addr = 'localhost'
    local_mqtt_port = 1883
    local_mqtt_client_id = 'asdfasdf'
    async with aiotmqtt.Client(local_mqtt_addr, local_mqtt_port) as client:
        client.publish('opus/discovery', json.dumps(
            {
                ""
            }
        )