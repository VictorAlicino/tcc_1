"""Sonoff API Light Implementation"""

import json
import logging
# Non-Standard Libraries
import aiohttp
from core.devices.light import OpusLight
from .sonoff_device import SonoffDevice # pylint: disable=import-error

log = logging.getLogger(__name__)


class SonoffLight(OpusLight):
    """Sonoff API Light Implementation"""
    def __init__(self, name: str, uuid: str, room_id: str, space_id: str, building: str):
        super().__init__(
            name=name,
            uuid=uuid,
            room_id=room_id,
            space_id=space_id,
            building=building,
            driver="sonoff"
        )
        self.link: SonoffDevice

    async def on(self) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    f'http://{self.link.ip_address}:{self.link.port}'
                    f'/zeroconf/switch',
                    # "{"deviceid": "10016d3258", "data": { "switch": "on" }}"
                    data= json.dumps({
                        "deviceid": self.link.device_id,
                        "data": { "switch": "on"}
                        })
                    ):
                #print(await resp.text())
                ...

    async def off(self) -> None:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                        f'http://{self.link.ip_address}:{self.link.port}'
                        f'/zeroconf/switch',
                        # "{"deviceid": "10016d3258", "data": { "switch": "off" }}"
                        data= json.dumps({
                            "deviceid": self.link.device_id,
                            "data": { "switch": "off"}
                            })
                        ):
                    ...
            except ConnectionError as e:
                log.error("Error: %s", e)

    async def toggle(self) -> None:
        """Toggle the Light On/Off"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                        f'http://{self.link.ip_address}:{self.link.port}'
                        f'/zeroconf/switch',
                        # "{"deviceid": "10016d3258", "data": { "switch": "toggle" }}"
                        data= json.dumps({
                            "deviceid": self.link.device_id,
                            "data": { "switch": f"{not self.power_state}"}
                            })
                        ):
                    ...
            except ConnectionError as e:
                print(f"Error: {e}")

    async def update_status(self) -> None:
        """Update the Status of the Light"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                        f'http://{self.link.ip_address}:{self.link.port}'
                        f'/zeroconf/info',
                        # "{"deviceid": "10016d3258", "data": {}}"
                        data= json.dumps({
                            "deviceid": self.link.device_id,
                            "data": {}
                            })
                        ) as resp:
                    log.debug(await resp.text())
            except ConnectionError as e:
                print(f"Error: {e}")

    def __str__(self):
        return (f"Sonoff Light -> \n"
                #f"Core Data:\n"
                #f"\tName: {super.name}\n"
                #f"\tID: {super.id}\n"
                #f"\tRoom ID: {super.room_id}\n"
                #f"\tSpace ID: {super.space_id}\n"
                #f"\tBuilding: {super.building}\n"
                #f"\tDriver: {super.driver}\n"
                f"Driver Data:\n"
                f"{self.link}")

async def create_sonoff_light(name: str, link: SonoffDevice) -> SonoffLight:
    """Create a new Sonoff Light"""
    log.debug("Registering new Sonoff Light: %s", name)
    new_light = SonoffLight(name, "", "", "", "")
    new_light.link = link
    device_payload: json = {}
    # Get the "device_id" which was not possible before
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                    f'http://{new_light.link.ip_address}:{new_light.link.port}'
                    f'/zeroconf/info',
                    data= json.dumps({
                        "deviceid": new_light.link.device_id,
                        "data": {}
                        })
                    ) as resp:
                device_payload = await resp.json()
        except Exception as e: #TODO: Change to a more specific exception #pylint: disable=broad-except
            log.error("Error: %s", e)        

    new_light.power_state = device_payload['data']['switch']
    new_light.link.device_id = device_payload['data']['deviceid']
    new_light.link.bssid = device_payload['data']['bssid']

    return new_light
