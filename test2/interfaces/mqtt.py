"""MQTT Interface"""
from threading import Lock, Thread
import logging
import paho.mqtt.client as mqtt

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

class MQTTClient(metaclass=SingletonMeta):
    """Singleton MQTT Client"""

    def __init__(self):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.thread: Thread
        log.debug("MQTT Initialized")

    def begin(self, config: dict):
        """Begin the MQTT Client"""
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        log.debug("Connecting to %s:%s", config['host'], config['port'])
        self.client.connect(config['host'], config['port'])

    def start_thread(self):
        """Start the MQTT Client Thread"""
        self.thread = Thread(target=self.client.loop_forever)
        self.thread.start()

    def stop_thread(self):
        """Stop the MQTT Client Thread"""
        self.client.loop_stop()

    def on_connect(self, client, userdata, flags, reason_code, properties): # pylint: disable=unused-argument
        """On Connect Callback"""
        print(f"Connected with result code {reason_code}")

    def on_message(self, client, userdata, msg): # pylint: disable=unused-argument
        """On Message Callback"""
        print(msg.topic+" "+str(msg.payload))

    def connect(self, host: str, port: int = 1883):
        """Connect to MQTT Broker"""
        self.client.connect(host, port, 60)

    def publish(self, topic: str, payload: str):
        """Publish a message"""
        self.client.publish(topic, payload)

    def subscribe(self, topic: str):
        """Subscribe to a topic"""
        self.client.subscribe(topic)

def initialize() -> MQTTClient:
    """Initialize the MQTT Interface"""
    return MQTTClient()

if __name__ == "__main__":
    # DEBUG PURPOSES ONLY
    client = initialize()
    client.begin({"host": "192.168.15.120", "port": 1883})
    client.start_thread()
