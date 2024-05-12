"""Tasmota Device Class"""
from ipaddress import ip_address

class TasmotaDevice:
    """Generic Tasmota Device"""
    def __init__(self, ip: ip_address):
        self.ip_address: ip_address = ip
        self.bssid: bytearray | None
        self.device_type: str
        self.mqtt = None
        self.mqtt_topic_prefix: str

    def __str__(self) -> str:
        return (f"Tasmota Device at {self.ip_address}\n"
                f" BSSID     -> {self.bssid}\n"
                f" DeviceType -> {self.device_type}\n")
