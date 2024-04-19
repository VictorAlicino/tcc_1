"""SONOFF Connection Driver"""

from enum import Enum
import requests

class SONOFFDeviceType(Enum):
    """Enumare for Sonoff Device Types avaiable for the DIY API"""
    DIY_PLUG = 0    # BASICR3 | RFR3 | MINI | MINIR2 | MINIR3
    DIYLIGHT = 1    # D1
    DIY_METER = 2   # SPM-Main
    DIY_LIGHT = 3   # B02-BL-A60 | B05-BL-A19 | B05-BL-A60

type sonoff_device_type_t = SONOFFDeviceType

class SONOFFdriver:
    """Driver to talk to Sonoff Devices with the DIY API enabled"""
    def __init__(self):
        self.ip_address: list[
            bytes,
            bytes,
            bytes,
            bytes
            ]
        self.hostname: str
        self.service_type: str
        self.device_type: sonoff_device_type_t


def discover_devices():
    ...
