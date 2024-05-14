"""General Sonoff Device Class"""
from enum import Enum
from ipaddress import ip_address

class SonoffDeviceType(Enum):
    """Enumerate for Sonoff Device Types"""
    DIY_PLUG = 0    # BASICR3 | RFR3 | MINI | MINIR2 | MINIR3
    DIYLIGHT = 1    # D1
    DIY_METER = 2   # SPM-Main
    DIY_LIGHT = 3   # B02-BL-A60 | B05-BL-A19 | B05-BL-A60

    # Not DIY mode (Encrypted)
    STRIP = 4
    PLUG = 5

type sonoff_device_type_t = SonoffDeviceType

class SonoffDevice:
    """Driver to talk to Sonoff Devices with the DIY API enabled"""
    def __init__(self, ip: ip_address):
        self.ip_address: ip_address = ip
        self.hostname: str
        self.port: int = 8081
        self.bssid: bytearray | None
        self.device_type: sonoff_device_type_t | str
        self.service_instace_name: str
        self.device_id: str
        self.startup_info_dump: dict = {}

    def __str__(self) -> str:
        return (f"Sonoff Device {self.hostname} at {self.ip_address}\n"
                f"\tIP Address: {self.ip_address}\n"
                f"\tHostname: {self.hostname}\n"
                f"\tPort: {self.port}\n"
                f"\tBSSID: {self.bssid}\n"
                f"\tDevice Type: {self.device_type}\n"
                f"\tService Instance Name: {self.service_instace_name}\n"
                f"\tDevice ID: {self.device_id}\n"
                f"\tStartup Info Dump below:\n{self.startup_info_dump}")
