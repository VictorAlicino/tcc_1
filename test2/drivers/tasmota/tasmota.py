import asyncio
import paho.mqtt.client as pubsubclient
from .tasmota_device import TasmotaDevice
from .tasmota_hvac import create_tasmota_hvac


known_devices: list[TasmotaDevice] = []
registered_devices: list[any] = []

# TODO: Find all devices

# TODO: Register new devices
async def register_device(device: TasmotaDevice) -> None:
    """Register a new Device"""
    match device.device_type:
        case "hvac":
            print("Found a HVAC Device")
            registered_devices.append(await create_tasmota_hvac("ablublé2", device))


async def debug_main() -> None:
    """USE FOR DEBUG PURPOSES ONLY"""
    ...

if __name__ == "__main__":
    asyncio.run(debug_main())
