"""SONOFF Connection Driver"""

import asyncio
from enum import Enum
from ipaddress import ip_address
# Non-Standard Libraries
from zeroconf import ServiceBrowser, Zeroconf

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

    def __str__(self) -> str:
        return (f"Sonoff Device {self.hostname} at {self.ip_address}\n"
                f" DeviceID              -> {self.device_id}\n"
                f" Type                  -> {self.device_type}\n"
                f" Port                  -> {self.port}\n"
                f" BSSID                 -> {self.bssid}\n"
                f" Service instance name -> {self.service_instace_name}\n")

known_devices: list = []

def _found_new_device(name, info) -> None:
    ip = info.addresses[0]
    new_device = SonoffDevice(ip_address(f'{ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}'))
    new_device.hostname = name.split('.')[0]
    new_device.port = info.port
    new_device.bssid = None
    new_device.device_type = bytes(info.properties[('type').encode('utf-8')]).decode()
    new_device.service_instace_name = info.type
    new_device.device_id = bytes(info.properties[('id').encode('utf-8')]).decode()
    #print(f"\n[mDNS] Found new {new_device.device_type} -> "
    #      f"{new_device.hostname} @ {new_device.ip_address}"
    #      f" | id: {new_device.device_id}")
    #print(properties)
    known_devices.append(new_device)


class MDNSListener:
    """Listener for Sonoff mDNS Service"""

    def remove_service(self, zeroconf, type, name): # pylint: disable=redefined-builtin
        """"Remove Service"""
        # do nothing

    def add_service(self, zeroconf, type, name): # pylint: disable=redefined-builtin
        """Add a Device to the known devices list"""
        info = zeroconf.get_service_info(type, name)
        if info:
            _found_new_device(name, info)


async def search_devices(timer: int) -> list[SonoffDevice]:
    """Search for Sonoff Devices in the network"""
    zeroconf = Zeroconf()
    listener = MDNSListener()
    ServiceBrowser(zeroconf, "_ewelink._tcp.local.", listener)

    await asyncio.sleep(timer)
    zeroconf.close()
    return known_devices
