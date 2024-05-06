"""MQTT Interface"""
from threading import Lock, Thread
import paho.mqtt.client as mqtt

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
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        """On Connect Callback"""
        print(f"Connected with result code {rc}")

    def on_message(self, client, userdata, msg):
        """On Message Callback"""
        print(f"{msg.topic} {str(msg.payload)}")

    def connect(self, host: str, port: int = 1883):
        """Connect to MQTT Broker"""
        self.client.connect(host, port, 60)

    def publish(self, topic: str, payload: str):
        """Publish a message"""
        self.client.publish(topic, payload)

    def subscribe(self, topic: str):
        """Subscribe to a topic"""
        self.client.subscribe(topic)
