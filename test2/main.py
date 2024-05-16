"""The main entry point for the application."""

import sys
import asyncio
from typing import Final
from core.device_manager import DeviceManager
from core.location_manager import LocationManager
import initializers

# Python Version
REQUIRED_PYTHON_VER: Final = (3, 12, 0)

# OS Supported
SUPPORTED_OS: Final = ["linux", "darwin", "win32"]

# Directories Path
DIRS: dict = {
    "CORE": "core",
    "INTERFACES": "interfaces",
    "CONFIG": "config",
    "DRIVERS": "drivers",
    "DATABASES": "db",
    "SERVER": "server",
}

# Global Configuration
CONFIG: dict = {}

# Drivers objects
DRIVERS: dict = {}

# Interfaces objects
INTERFACES: dict = {}

# Devices Manager
D_MANAGER = None

# Location Manager
L_MANAGER = None


async def main() -> None:
    """The main function."""
    await DRIVERS['sonoff'].start()
    await asyncio.sleep(2)
    print(f'Sonoff Get Known Devices: {DRIVERS['sonoff'].get_known_devices()}')
    luz1 = await DRIVERS['sonoff'].create_sonoff_light(
        "Luz1",
        DRIVERS['sonoff'].get_known_devices()[0]
        )
    #INTERFACES['mqtt'].start_thread()
    D_MANAGER.new_device(luz1)
    D_MANAGER.print_all_devices()
    while True:
        await asyncio.sleep(0.001)
        await luz1.on()
        await asyncio.sleep(1)
        await luz1.off()
        await asyncio.sleep(1)


if __name__ == "__main__":
    exit_code: int = 0

    initializers.define_log()
    initializers.check_python(REQUIRED_PYTHON_VER)
    initializers.check_os(SUPPORTED_OS)
    initializers.check_directories(DIRS)
    CONFIG = initializers.load_configurations()
    initializers.load_interfaces(config=CONFIG, dirs=DIRS, interfaces=INTERFACES)
    initializers.load_drivers(config=CONFIG, dirs=DIRS, drivers=DRIVERS, interfaces=INTERFACES)

    D_MANAGER = DeviceManager(DIRS)
    L_MANAGER = LocationManager()

    # (INTERFACES)
    # TODO: Start devices manager

    # TODO: Connect to database
    # TODO: Start event manager
    # TODO: Start task manager
    try:
        asyncio.run(main())
    except KeyboardInterrupt as e:
        INTERFACES['mqtt'].stop_thread()
        print(e)
    sys.exit(exit_code)
