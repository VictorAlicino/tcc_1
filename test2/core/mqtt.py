"""Communication handler"""

from dataclasses import dataclass
from typing import Literal as typing_literal
from paho.mqtt.properties import Properties as paho_mqtt_properties
from paho.mqtt.client import Client as paho_mqtt_client

@dataclass
class MQTTConfig:
    """MQTT communication specific configurations data type"""
    # Note that this does follow the required arguments by
    # PAHO implementation.
    keep_alive: int | None
    bind_address: str | None
    bind_port: str | None
    clean_start: bool | typing_literal[3] | None
    properties: paho_mqtt_properties | None
type mqtt_config_t = MQTTConfig


class MQTT:
    """Communication handler"""

    def __init__(self):
        self.broker_host: str = None
        self.broker_port: str = None
        self.secure_connection: bool = True
        self.mqtt_config: mqtt_config_t = None

        self.client: paho_mqtt_client = None

    def connect(self) -> None:
        ...
