"""Sonoff API Light Implementation"""

import sys
import asyncio
import json
from ipaddress import ip_address
# Non-Standard Libraries
sys.path.append('../../') # pylint: disable=wrong-import-position
import aiohttp
from sonoff import SonoffDevice # pylint: disable=import-error
from core.devices.light import OpusLight

class SonoffLight(OpusLight):
    """Sonoff API Light Implementation"""
    def __init__(self, device_name: str):
        super().__init__()
        self.name = device_name
        self.sonoff_link: SonoffDevice

    async def on(self) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    f'http://{self.sonoff_link.ip_address}:{self.sonoff_link.port}/zeroconf/switch',
                    # "{"deviceid": "10016d3258", "data": { "switch": "on" }}"
                    data= json.dumps({
                        "deviceid": self.sonoff_link.device_id,
                        "data": { "switch": "on"}
                        })
                    ) as resp:
                    print(resp)

    async def off(self) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    f'http://{self.sonoff_link.ip_address}:{self.sonoff_link.port}/zeroconf/switch',
                    # "{"deviceid": "10016d3258", "data": { "switch": "off" }}"
                    data= json.dumps({
                        "deviceid": self.sonoff_link.device_id,
                        "data": { "switch": "off"}
                        })
                    ) as resp:
                    print(resp)

async def debug() -> int:
    """Main for Debug porpuses"""
    luz1 = SonoffLight("ablublé")
    luz1.sonoff_link = SonoffDevice(ip_address("192.168.15.2"))
    luz1.sonoff_link.device_id = "10016d3258"
    luz1.sonoff_link.hostname = "eWeLink_10016d3258._ewelink._tcp.local."

    #await luz1.on()
    #await asyncio.sleep(2)
    #await luz1.off()
    #await asyncio.sleep(2)
    return 0

if __name__ == "__main__":
    try:
        while True:
            try:
                asyncio.run(debug())
            except Exception as e:
                print(f"Error: {e}")
                raise e
    except KeyboardInterrupt:
        sys.exit(127)
