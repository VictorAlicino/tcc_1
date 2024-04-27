"""SONOFF Connection Driver"""

import asyncio
import sys
from ipaddress import ip_address
# Non-Standard Libraries
from zeroconf import ServiceBrowser, Zeroconf
from .sonoff_device import SonoffDevice
from .sonoff_light import create_sonoff_light, SonoffLight

known_devices: list[SonoffDevice] = []
registered_devices: list = []

def get_known_devices() -> list[SonoffDevice]:
    """Get the known devices"""
    return known_devices

def get_registered_devices() -> list:
    """Get the registered devices"""
    return registered_devices

def _found_new_device(name, info) -> None:
    ip = info.addresses[0]
    new_device = SonoffDevice(ip_address(f'{ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}'))
    new_device.hostname = name.split('.')[0]
    new_device.port = info.port
    new_device.bssid = None
    new_device.device_type = bytes(info.properties[('type').encode('utf-8')]).decode()
    new_device.service_instace_name = info.type
    new_device.device_id = bytes(info.properties[('id').encode('utf-8')]).decode()
    new_device.startup_info_dump = info.properties

    known_devices.append(new_device)

async def register_device(device: SonoffDevice) -> None:
    """Register a new Device"""
    match device.device_type:
        case "diy_plug":
            print("Found a DIY Plug")
            registered_devices.append(await create_sonoff_light("ablublé", device))

sonoff_discovered_devices: list = []

class MDNSListener:
    """Listener for Sonoff mDNS Service"""

    def remove_service(self, zeroconf, type, name): # pylint: disable=redefined-builtin
        """"Remove Service"""
        # do nothing

    def update_service(self, zeroconf, type, name): # pylint: disable=redefined-builtin, unused-argument
        """Update Service"""
        #print(f'Update Service {name} {type}')
        info = zeroconf.get_service_info(type, name)
        if info:
            if (info.properties.get(b'id').decode() in
            [device.device_id for device in known_devices]):
                print(f"Device {info.properties.get(b'id').decode()} state changed")

    def add_service(self, zeroconf, type, name): # pylint: disable=redefined-builtin
        """Add a Device to the known devices list"""
        info = zeroconf.get_service_info(type, name)
        if info and info.properties.get(b'encrypt') is None:
            _found_new_device(name, info)


async def start_sonoff_finder() -> list[SonoffDevice]:
    """Search for Sonoff Devices in the network"""
    zeroconf = Zeroconf()
    listener = MDNSListener()
    ServiceBrowser(zeroconf, "_ewelink._tcp.local.", listener)

    return known_devices

async def start() -> None:
    """Main Function"""
    await start_sonoff_finder()

async def main_debug() -> None:
    """Main for Debug porpuses"""
    luz1 = SonoffLight("ablublé")
    luz1.sonoff_link = SonoffDevice(ip_address("192.168.15.2"))
    luz1.sonoff_link.device_id = "10016d3258"
    luz1.sonoff_link.hostname = "eWeLink_10016d3258._ewelink._tcp.local."

    await start_sonoff_finder()
    await asyncio.sleep(1)
    for device in known_devices:
        await register_device(device)
    print(registered_devices)
    while True:
        for device in registered_devices:
            try:
                await device.on()
                await asyncio.sleep(2)
                await device.off()
                await asyncio.sleep(2)
            except Exception as e:
                print(f"Error: {e}")
                raise e

if __name__ == "__main__":
    asyncio.run(main_debug())
