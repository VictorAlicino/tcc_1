"""Sonoff API Light Implementation"""

import sys
import json
# Non-Standard Libraries
sys.path.append('../../') # pylint: disable=wrong-import-position
import aiohttp
from sonoff_device import SonoffDevice # pylint: disable=import-error
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
                    f'http://{self.sonoff_link.ip_address}:{self.sonoff_link.port}'
                    f'/zeroconf/switch',
                    # "{"deviceid": "10016d3258", "data": { "switch": "on" }}"
                    data= json.dumps({
                        "deviceid": self.sonoff_link.device_id,
                        "data": { "switch": "on"}
                        })
                    ) as resp:
                #print(await resp.text())
                ...

    async def off(self) -> None:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                        f'http://{self.sonoff_link.ip_address}:{self.sonoff_link.port}'
                        f'/zeroconf/switch',
                        # "{"deviceid": "10016d3258", "data": { "switch": "off" }}"
                        data= json.dumps({
                            "deviceid": self.sonoff_link.device_id,
                            "data": { "switch": "off"}
                            })
                        ) as resp:
                    #print(await resp.text())
                    ...
            except ConnectionError as e:
                print(f"Error: {e}")

    async def update_status(self) -> None:
        """Update the Status of the Light"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                        f'http://{self.sonoff_link.ip_address}:{self.sonoff_link.port}'
                        f'/zeroconf/info',
                        # "{"deviceid": "10016d3258", "data": {}}"
                        data= json.dumps({
                            "deviceid": self.sonoff_link.device_id,
                            "data": {}
                            })
                        ) as resp:
                    print(await resp.text())
            except ConnectionError as e:
                print(f"Error: {e}")

    def __str__(self):
        return (f"Sonoff Light {self.sonoff_link.device_id}@"
                f"{self.sonoff_link.ip_address}|{self.sonoff_link.bssid} ")

async def create_sonoff_light(name: str, link: SonoffDevice) -> SonoffLight:
    """Create a new Sonoff Light"""
    print(f"Registering new Sonoff Light: {name}")
    new_light = SonoffLight(name)
    new_light.sonoff_link = link
    device_payload: json = {}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                    f'http://{new_light.sonoff_link.ip_address}:{new_light.sonoff_link.port}'
                    f'/zeroconf/info',
                    data= json.dumps({
                        "deviceid": new_light.sonoff_link.device_id,
                        "data": {}
                        })
                    ) as resp:
                device_payload = await resp.json()
        except Exception as e:
            print(f"Error: {e}")

    new_light.power_state = device_payload['data']['switch']
    new_light.sonoff_link.device_id = device_payload['data']['deviceid']
    new_light.sonoff_link.bssid = device_payload['data']['bssid']

    return new_light
