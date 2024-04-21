"""SONOFF Connection Driver"""

from enum import Enum
import sys
from ipaddress import ip_address
# Non-Standard Libraries
from zeroconf import ServiceBrowser, Zeroconf

class SonoffDeviceType(Enum):
    """Enumerate for Sonoff Device Types available for the DIY API"""
    DIY_PLUG = 0    # BASICR3 | RFR3 | MINI | MINIR2 | MINIR3
    DIYLIGHT = 1    # D1
    DIY_METER = 2   # SPM-Main
    DIY_LIGHT = 3   # B02-BL-A60 | B05-BL-A19 | B05-BL-A60

type sonoff_device_type_t = SonoffDeviceType

class SonoffDevice:
    """Driver to talk to Sonoff Devices with the DIY API enabled"""
    def __init__(self, ip: ip_address):
        self.ip_address: ip_address = ip
        self.hostname: str
        self.port: int = 8081
        self.bssid: bytearray
        self.device_type: sonoff_device_type_t
        self.service_instace_name: str
        self.device_id: str

    def __str__(self) -> str:
        return (f"Sonoff Device {self.hostname} at {self.ip_address}"
                f" with device_id {self.device_id}"
                f" and type {self.device_type.name}"
                f" on port {self.port}"
                f" with BSSID {self.bssid.hex()}"
                f" and service instance name {self.service_instace_name}")

known_devices: list = []

async def search_devices() -> list[SonoffDevice]:
    """Search for Sonoff Devices in the network"""

class MDNSListener:
    """Listener for Sonoff mDNS Service"""

    def remove_service(self, zeroconf, type, name):
        """"Remove Service"""
        # do nothing

    def add_service(self, zeroconf, type, name):
        """Add a Device to the known devices list"""
        if type == "_ewelink._tcp.local.":
            info = zeroconf.get_service_info(type, name)
            if info:
                ip = info.addresses[0]
                new_device = SonoffDevice(ip_address(f'{ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}'))
                new_device.hostname = name
                new_device.port = info.port
                new_device.service_instace_name = info.type
                print(f"Found device {new_device.hostname} at {new_device.ip_address}")
                print(info)
                known_devices.append(new_device)

zeroconf = Zeroconf()
listener = MDNSListener()
browser = ServiceBrowser(zeroconf, "_ewelink._tcp.local.", listener)

try:
    input("Press enter to stop discovering...\n")
finally:
    zeroconf.close()

print("Discovered devices with ewelink service:")
for device in known_devices:
    print(device)
    print()

sys.exit(0)
