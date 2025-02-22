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
        self.temperature: float = 20.0

        self.power_state = "Off"
        self.fan_speed = "Auto"
        self.mode = "Cool"
        self.temperature = 24.0

    def on(self) -> None:
        """Turn the HVAC on"""
        log.info("Turning on HVAC %s @ %s", self.name, self.room_id)
        self.mqtt_link.publish(
            topic=f"cmnd/{self.mqtt_name}/IRHVAC",
            payload=json.dumps({
                "Vendor": self.vendor,
                "Power": "On",
                "Mode": self.mode,
                "FanSpeed":3,
                "Temp": self.temperature
            })
        )
        self.power_state = "On"


    def off(self) -> None:
        """Turn the HVAC off"""
        log.info("Turning off HVAC %s @ %s", self.name, self.room_id)
        self.mqtt_link.publish(
            topic=f"cmnd/{self.mqtt_name}/IRHVAC",
            payload=json.dumps({
                "Vendor": self.vendor,
                "Power": "Off",
                "Mode": self.mode,
                "Temp": self.temperature
            })
        )
        self.power_state = "Off"

    def set_temperature(self, temperature: float) -> None:
        """Set the Temperature"""
        log.info("Setting temperature of %s to %s @ %s", self.name, temperature, self.room_id)
        self.mqtt_link.publish(
            topic=f"cmnd/{self.mqtt_name}/IRHVAC",
            payload=json.dumps({
                "Vendor": self.vendor,
                "Power": self.power_state,
                "Mode": self.mode,
                "Temp": temperature
            })
        )
        self.temperature = temperature

    def set_mode(self, mode: str) -> None:
        """Set the Mode"""
        log.info("Setting mode of %s to %s @ %s", self.name, mode, self.room_id)
        self.mqtt_link.publish(
            topic=f"cmnd/{self.mqtt_name}/IRHVAC",
            payload=json.dumps({
                "Vendor": self.vendor,
                "Power": self.power_state,
                "Mode": mode,
                "Temp": self.temperature
            })
        )
        self.mode = mode

    def set_fan_speed(self, fan_speed: str) -> None:
        """Set the Fan Speed"""
        log.info("Setting fan speed of %s to %s @ %s", self.name, fan_speed, self.room_id)
        self.mqtt_link.publish(
            topic=f"cmnd/{self.mqtt_name}/IRHVAC",
            payload=json.dumps({
                "Vendor": self.vendor,
                "Power": self.power_state,
                "Mode": self.mode,
                "FanSpeed": fan_speed,
                "Temp": self.temperature
            })
        )
        self.fan_speed = fan_speed

    def set_state(self, state: dict) -> None:
        """Set the state of the HVAC"""
        log.info("Setting state of %s to %s @ %s", self.name, state, self.room_id)
        self.mqtt_link.publish(
            topic=f"cmnd/{self.mqtt_name}/IRHVAC",
            payload=json.dumps({
                "Power": state.get("power_state", self.power_state),
                "Mode": state.get("mode", self.mode),
                "FanSpeed": state.get("fan_speed", self.fan_speed),
                "Temp": state.get("temperature", self.temperature)
            })
        )
        self.power_state = state.get("power_state", self.power_state)
        self.mode = state.get("mode", self.mode)
        self.fan_speed = state.get("fan_speed", self.fan_speed)
        self.temperature = float(state.get("temperature", self.temperature))
        self.print_state()

    def print_data(self) -> None:
        """Print the HVAC Data"""
        log.debug("Name: %s", self.name)
        log.debug("\t├── ID: %s", self.id)
        log.debug("\t├── Room ID: %s", self.room_id)
        log.debug("\t├── Space ID: %s", self.space_id)
        log.debug("\t├── Building ID: %s", self.building_id)
        log.debug("\t├── Driver: %s", self.driver)
        log.debug("\t├── Vendor: %s", self.vendor)
        log.debug("\t├── MQTT Name: %s", self.mqtt_name)
        log.debug("\t└── Type: %s", self.type)

    def print_state(self) -> None:
        """Print the HVAC State"""
        log.debug("Name: %s", self.name)
        log.debug("\t├── Power State: %s", self.power_state)
        log.debug("\t├── Mode: %s", self.mode)
        log.debug("\t├── Fan Speed: %s", self.fan_speed)
        log.debug("\t└── Temperature: %s", self.temperature)