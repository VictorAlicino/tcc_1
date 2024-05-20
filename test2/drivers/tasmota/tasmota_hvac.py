"""Tasmota HVAC Integration"""
#Non standard libraries
from uuid import UUID
import json
import logging
from interfaces.mqtt import MQTTClient
from core.devices.hvac import OpusHVAC
from .tasmota_device import TasmotaDevice

log = logging.getLogger(__name__)

class TasmotaHVAC(OpusHVAC):
    """Tasmota HVAC Implementation"""
    def __init__(self,
                 name: str,
                 tasmota_device: TasmotaDevice,
                 mqtt_link: MQTTClient):
        super().__init__(
            name=name,
            uuid=UUID(str(tasmota_device.id)),
            driver="tasmota"
        )
        self.mqtt_link = mqtt_link
        self.mqtt_name: str = tasmota_device.tasmota_name

    def on(self) -> None:
        """Turn the light on"""
        print("Turning on HVAC")
        self.mqtt_link.publish(
            topic=f"cmnd/{self.mqtt_name}/IRHVAC",
            payload=json.dumps({
                "Vendor": self.vendor,
                "Power": "On",
                "Mode": self.mode,
                "FanSpeed": self.fan_speed,
                "Temp": self.temperature
            })
        )
        self.power_state = "On"


    def off(self) -> None:
        """Turn the light off"""
        print("Turning off HVAC")
        self.mqtt_link.publish(
            topic=f"cmnd/{self.mqtt_name}/IRHVAC",
            payload=json.dumps({
                "Vendor": self.vendor,
                "Power": "Off",
                "Mode": self.mode,
                "FanSpeed": self.fan_speed,
                "Temp": self.temperature
            })
        )
        self.power_state = "Off"

    def set_temperature(self, temperature: float) -> None:
        """Set the Temperature"""
        print(f"Setting Temperature to {temperature}")
        self.mqtt_link.publish(
            topic=f"cmnd/{self.mqtt_name}/IRHVAC",
            payload=json.dumps({
                "Vendor": self.vendor,
                "Power": self.power_state,
                "Mode": self.mode,
                "FanSpeed": self.fan_speed,
                "Temp": temperature
            })
        )

    def print_data(self) -> None:
        """Print the HVAC Data"""
        log.debug("Name: %s", self.name)
        log.debug("\t├── ID: %s", self.id)
        log.debug("\t├── Room ID: %s", self.room_id)
        log.debug("\t├── Space ID: %s", self.space_id)
        log.debug("\t├── Building ID: %s", self.building_id)
        log.debug("\t├── Driver: %s", self.driver)
        log.debug("\t└── Type: %s", self.type)
