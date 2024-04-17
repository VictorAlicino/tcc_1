"""Communication handler"""

from paho.mqtt import client
from paho.mqtt.enums import CallbackAPIVersion


class MQTT:
    """Communication handler"""

    def __init__(self, client_name: str):
        # MQTT Client Configuration (see PAHO MQTT Docs)
        self.client = client.Client(
            callback_api_version= CallbackAPIVersion.VERSION2,
            client_id=client_name,
            clean_session=True,
            userdata=None,
            protocol=client.MQTTv5,
            transport='tcp',
            reconnect_on_failure=True,
            manual_ack=False
        )

    def config(self, )
