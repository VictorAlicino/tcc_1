"""SONOFF Connection Driver"""

from enum import Enum
from ipaddress import ip_address
import requests

class SONOFFDeviceType(Enum):
    """Enumerate for Sonoff Device Types available for the DIY API"""
    DIY_PLUG = 0    # BASICR3 | RFR3 | MINI | MINIR2 | MINIR3
    DIYLIGHT = 1    # D1
    DIY_METER = 2   # SPM-Main
    DIY_LIGHT = 3   # B02-BL-A60 | B05-BL-A19 | B05-BL-A60

type sonoff_device_type_t = SONOFFDeviceType

class SonoffDevice:
    """Driver to talk to Sonoff Devices with the DIY API enabled"""
    def __init__(self, ip: ip_address):
        self.ip_address: ip_address = ip
        self.hostname: str
        self.service_type: str
        self.device_type: sonoff_device_type_t
        self.service_instace_name: str

