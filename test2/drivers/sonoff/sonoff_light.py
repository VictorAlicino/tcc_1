"""Sonoff API Light Implementation"""

import json
import logging
from uuid import UUID
from ipaddress import ip_address
# Non-Standard Libraries
import aiohttp
import requests
from core.devices.light import OpusLight
from .sonoff_device import SonoffDevice # pylint: disable=import-error

log = logging.getLogger(__name__)


class SonoffLight(OpusLight):
    """Sonoff API Light Implementation"""
    def __init__(self,
                 name: str,
                 sonoff_device: SonoffDevice):
        super().__init__(
            name=name,
            uuid=UUID(str(sonoff_device.id)),
            driver="sonoff"
        )
        self.ip_address: ip_address = ip_address(sonoff_device.ip_address)
        self.hostname: str = str(sonoff_device.hostname)
        self.port: int = int(sonoff_device.port)
        self.device_id: str
        self.startup_info_dump: dict = {}

        # Get the "device_id" which was not possible before
        device_payload = requests.post(
            url=f'http://{self.ip_address}:{self.port}/zeroconf/info',
            data= json.dumps({
                "deviceid": "",
                "data": {}
                }),
            headers={"Content-Type": "application/json"},
            timeout=5
            )
        device_payload = device_payload.json()

        self.power_state = device_payload['data']['switch']
        self.device_id = device_payload['data']['deviceid']
        self.bssid = device_payload['data']['bssid']

    def on(self) -> None:
        requests.post(
            url=f'http://{self.ip_address}:{self.port}/zeroconf/switch',
            data= json.dumps({
                "deviceid": self.device_id,
                "data": { "switch": "on"}
                }),
            headers={"Content-Type": "application/json"},
            timeout=5
        )

    def off(self) -> None:
        requests.post(
            url=f'http://{self.ip_address}:{self.port}/zeroconf/switch',
            data= json.dumps({
                "deviceid": self.device_id,
                "data": { "switch": "off"}
                }),
            headers={"Content-Type": "application/json"},
            timeout=5
        )

    def toggle(self) -> None:
        """Toggle the Light On/Off"""
        requests.post(
            url=f'http://{self.ip_address}:{self.port}/zeroconf/switch',
            data= json.dumps({
                "deviceid": self.device_id,
                "data": { "switch": "toggle"}
                }),
            headers={"Content-Type": "application/json"},
            timeout=5
        )

    def update_status(self) -> None:
        """Update the Status of the Light"""
        resp = requests.post(
            url=f'http://{self.ip_address}:{self.port}/zeroconf/info',
            data= json.dumps({
                "deviceid": self.device_id,
                "data": {}
                }),
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        resp = resp.json()
        self.power_state = resp[b'data'][b'switch']
        log.debug("%s Power State: %s", self.name, resp[b'data'][b'switch'])

    def print_data(self) -> None:
        """Print the Light Data"""
        log.debug("Name: %s", self.name)
        log.debug("\t├── ID: %s", self.id)
        log.debug("\t├── Room ID: %s", self.room_id)
        log.debug("\t├── Space ID: %s", self.space_id)
        log.debug("\t├── Building ID: %s", self.building_id)
        log.debug("\t├── Driver: %s", self.driver)
        log.debug("\t├── Type: %s", self.type)
        log.debug("\t├── IP Address: %s", self.ip_address)
        log.debug("\t├── Hostname: %s", self.hostname)
        log.debug("\t├── Port: %s", self.port)
        log.debug("\t├── Device ID: %s", self.device_id)
        log.debug("\t├── Power State: %s", self.power_state)
        log.debug("\t└── BSSID: %s", self.bssid)
