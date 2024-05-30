"""Tasmota Driver Main"""
import logging
import json
import uuid
from core.device_manager import DeviceManager
from interfaces.mqtt import MQTTClient
from .tasmota_device import TasmotaDevice
from .tasmota_hvac import TasmotaHVAC
# from .tasmota_hvac import create_tasmota_hvac

log = logging.getLogger(__name__)

interfaces: dict[str, any] = {'mqtt<local>': None}

OPUS_D_MANAGER: DeviceManager = None
MQTT_DRIVER: MQTTClient = None

def new_hvac(name: str, base_device: TasmotaDevice, additional_data) -> TasmotaHVAC:
    """Create a new Tasmota HVAC"""
    new = TasmotaHVAC(name,
                      base_device,
                      MQTT_DRIVER
                    )
    new.vendor = additional_data['data']['vendor']
    log.debug("Registering new Tasmota HVAC: %s", name)
    return new

def _mqtt_callback(topic, data: json) -> None:
    """Callback for new devices"""
    log.debug("Tasmota -> MQTT Callback")
    match topic[3]:
        case "new_device":
            log.debug("Tasmota -> New device Requested")
            print(data)
            match data["device_type"]:
                case "HVAC":
                    log.debug("Creating new Tasmota HVAC")
                    new_device = TasmotaDevice()
                    new_device.id = uuid.uuid1()
                    new_device.tasmota_name = data['data']["tasmota_name"]
                    new_device.type = "HVAC"
                    OPUS_D_MANAGER.new_device(new_device)
                    OPUS_D_MANAGER.register_device(
                        device_id=uuid.UUID(str(new_device.id)),
                        device_name=data["device_name"],
                        device_driver="tasmota",
                        room_id=uuid.UUID(str(data["room_id"])),
                        additional_data=data
                    )
                case _:
                    log.error("Unknown Device Type: %s", data["device_type"])

def load_hvac(name: str, driver_data: dict) -> TasmotaHVAC:
    """Load a Tasmota HVAC"""
    log.debug("Loading Tasmota HVAC: %s", name)
    temp_obj = TasmotaDevice()
    temp_obj.id = uuid.UUID(driver_data['id'])
    temp_obj.tasmota_name = driver_data['tasmota_name']
    temp_obj.type = driver_data['device_type']
    new = TasmotaHVAC(name, temp_obj, MQTT_DRIVER)
    new.vendor = driver_data['vendor']
    return new

def start(dirs: dict,
          config: dict,
          drivers: dict,
          interfaces: dict,
          managers: dict) -> None:
    """Main Function"""
    log.debug("Starting Tasmota Driver")
    global OPUS_D_MANAGER # pylint: disable=global-statement
    global MQTT_DRIVER # pylint: disable=global-statement
    OPUS_D_MANAGER = managers['devices']
    MQTT_DRIVER = interfaces['mqtt<local>']
