"""Tasmota Device Class"""
from ipaddress import ip_address
from core.devices.__generic import OpusDevice

class TasmotaDevice(OpusDevice):
    """Generic Tasmota Device"""
    def __init__(self):
        super().__init__()
        self.driver = "tasmota"
        self.tasmota_name: str
        self.mqtt_topic: str

    def __str__(self) -> str:
        return f"<TasmotaDevice-{self.tasmota_name}>"

