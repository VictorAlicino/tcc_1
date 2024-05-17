"""The main entry point for the application."""

import sys
import asyncio
from types import ModuleType
from typing import Final
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
DRIVERS: dict[ModuleType] = {}

# Interfaces objects
INTERFACES: dict[ModuleType] = {}

async def main() -> None:
    """The main function."""    
    await DRIVERS['sonoff'].start()
    await asyncio.sleep(2)
    print(DRIVERS['sonoff'].get_known_devices())
    luz1 = await DRIVERS['sonoff'].create_sonoff_light(
        "Luz1",
        DRIVERS['sonoff'].get_known_devices()[0]
        )
    print(luz1)
    INTERFACES['mqtt'].start_thread()
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
    #print(INTERFACES)
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
