"""Tasmota Driver Main"""
import logging
from .tasmota_device import TasmotaDevice
# from .tasmota_hvac import create_tasmota_hvac

log = logging.getLogger(__name__)

interfaces: dict[str, any] = {'mqtt<local>': None}
# TODO: Find all devices

# TODO: Register new devices
async def register_device(device: TasmotaDevice) -> None:
    """Register a new Device"""
    match device.device_type:
        case "hvac":
            print("Found a HVAC Device")


def start(dirs: dict,
          config: dict,
          drivers: dict,
          interfaces: dict,
          managers: dict) -> None:
    """Main Function"""
    log.debug("Starting Tasmota Driver")
