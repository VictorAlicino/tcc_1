"""Tasmota HVAC Integration"""
#Non standard libraries
from core.devices.hvac import OpusHVAC
from .tasmota_device import TasmotaDevice


class TasmotaHVAC(OpusHVAC):
    """Tasmota HVAC Implementation"""
    def __init__(self, name: str):
        super().__init__()
        super().name = name
        self.link: TasmotaDevice
        self.mqt_topic_prefix: str = ""

    async def on(self) -> None:
        """Turn the light on"""
        print("Turning on HVAC")
        # TODO: Implement the MQTT Logic

    async def off(self) -> None:
        """Turn the light off"""
        print("Turning off HVAC")
        # TODO: Implement the MQTT Logic

    async def set_temperature(self, temperature: float) -> None:
        """Set the Temperature"""
        print(f"Setting Temperature to {temperature}")
        # TODO: Implement the MQTT Logic

async def create_tasmota_hvac(name: str, link: TasmotaDevice) -> TasmotaHVAC:
    """Create a new Tasmota HVAC Device"""
    new_hvac = TasmotaHVAC(name)
    new_hvac.link = link
    return new_hvac
