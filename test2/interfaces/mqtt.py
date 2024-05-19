"""MQTT Interface"""
from threading import Lock, Thread
import logging
import paho.mqtt.client as mqtt
from getmac import get_mac_address as gma

log = logging.getLogger(__name__)

class SingletonMeta(type):
    """Singleton Metaclass"""
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]

class MQTTClient():
    """MQTT Client"""
    def __init__(self):
        self.client_id = f'opus-server-{gma()[-5:].replace(":", "")}'
        self.client = mqtt.Client(
            callback_api_version= mqtt.CallbackAPIVersion.VERSION2,
            client_id=self.client_id,
            userdata=None,
            protocol=mqtt.MQTTv5,
            transport='tcp',
            reconnect_on_failure=True,
            manual_ack=False
        )
        self.thread: Thread
        self.log_id = None
        log.info("MQTT Initialized")

    def begin(self, config: dict) -> bool:
        """Begin the MQTT Client"""
        self.log_id = config['log_id']
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        log.info("Connecting to %s:%s as %s", config['host'], config['port'], self.client_id)
        try:
            self.client.connect(config['host'], config['port'])
            self.subscribe(f'{self.client_id}/#')
            return True
        except TimeoutError as exp:
            log.error("Could not connect to %s:%s", config['host'], config['port'])
            log.error(exp)
            return False
        except ConnectionRefusedError as exp:
            log.error("Connection Refused to %s:%s", config['host'], config['port'])
            log.error(exp)
            return False

    def start_thread(self):
        """Start the MQTT Client Thread"""
        self.thread = Thread(target=self.client.loop_forever)
        self.thread.start()

    def stop_thread(self):
        """Stop the MQTT Client Thread"""
        self.client.loop_stop()

    def on_connect(self, client, userdata, flags, reason_code, properties): # pylint: disable=unused-argument
        """On Connect Callback"""
        log.info("%s connected with result code %s", self.log_id, reason_code)

    def on_message(self, client, userdata, msg): # pylint: disable=unused-argument
        """On Message Callback"""
        log.debug("%s Message Received: %s %s", self.log_id, msg.topic, msg.payload)

    def connect(self, host: str, port: int = 1883):
        """Connect to MQTT Broker"""
        self.client.connect(host, port, 60)

    def publish(self, topic: str, payload: str):
        """Publish a message"""
        self.client.publish(topic, payload)

    def register_callback(self, topic: str, callback):
        """Register a callback for a topic"""
        self.client.message_callback_add(
            f'{self.client_id}/{topic}',
            callback)
        log.debug("%s Callback Registered for %s", self.log_id, topic)

    def subscribe(self, topic: str):
        """Subscribe to a topic"""
        self.client.subscribe(topic)
        log.debug("Subscribed to %s", topic)

def initialize() -> MQTTClient:
    """Initialize the MQTT Interface"""
    return MQTTClient()

if __name__ == "__main__":
    # DEBUG PURPOSES ONLY
    client = initialize()
    client.begin({"host": "192.168.15.120", "port": 1883})
    client.start_thread()
