"""Devices Manager"""
import os

class DeviceManager():
    """Devices Manager"""
    def __init__(self):
        self.devices: dict = {} # This is gonna be hella big

    def devices_init(self) -> None:
        """Initialize the devices"""
        print("Initializing devices...")
        for file in os.listdir("./core/devices"):
            if file == "__init__.py" or not file.endswith(".py"):
                continue
            self.devices[file[:-3]] = {}
            setattr(self, f'opus_{file[:-3]}', {})
        print("Devices initialized!")

    def print_all_devices(self) -> None:
        """Print all devices"""
        for attr in dir(self):
            if attr.startswith("opus_"):
                print(f'{attr} -> {getattr(self, attr)}')
