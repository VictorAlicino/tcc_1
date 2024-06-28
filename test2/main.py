"""The main entry point for the application."""

import sys
import asyncio
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
    "LOGS": "logs",
}

# Global Configuration
CONFIG: dict = {}

# Drivers objects
DRIVERS: dict = {}

# Interfaces objects
INTERFACES: dict = {}

# Managers
MANAGERS: dict = {
    "devices": None,
    "locations": None,

}

async def main() -> None:
    """The main function."""
    #MANAGERS["locations"].dump_buildings()
    #MANAGERS["locations"].dump_rooms()
    #MANAGERS["locations"].new_building("Casa1")
    #MANAGERS["locations"].new_space("Patio", MANAGERS["locations"].get_building("Igreja").id)
    #MANAGERS["locations"].new_room("Portão", MANAGERS["locations"].get_space("Patio").id)
    #await DRIVERS['sonoff'].start(MANAGERS["devices"])
    INTERFACES['mqtt<local>'].start_thread()
    INTERFACES['mqtt<maestro>'].start_thread()
    #MANAGERS["devices"].print_all_devices()
    while True:
        await asyncio.sleep(1)
        #MANAGERS["devices"].get_device("59e900d215a811efacf9001a7dda710a").on()
        #await asyncio.sleep(1)
        #MANAGERS["devices"].get_device("59e900d215a811efacf9001a7dda710a").off()
        #await asyncio.sleep(1)


if __name__ == "__main__":
    exit_code: int = 0

    initializers.define_log(DIRS, log_level="DEBUG")
    initializers.check_python(REQUIRED_PYTHON_VER)
    initializers.check_os(SUPPORTED_OS)
    initializers.check_directories(DIRS)
    CONFIG = initializers.load_configurations()
    initializers.load_db(DIRS, INTERFACES)
    initializers.load_interfaces(
        config=CONFIG,
        dirs=DIRS,
        interfaces=INTERFACES
    )
    initializers.load_managers(
        dirs=DIRS,
        managers=MANAGERS,
        interfaces=INTERFACES,
        drivers=DRIVERS
    )
    initializers.load_drivers(
        config=CONFIG,
        dirs=DIRS,
        drivers=DRIVERS,
        interfaces=INTERFACES,
        managers=MANAGERS
    )
    MANAGERS["devices"].load_devices_from_db()

    # (INTERFACES)
    # TODO: Start devices manager

    # TODO: Connect to database
    # TODO: Start event manager
    # TODO: Start task manager
    try:
        asyncio.run(main())
    except KeyboardInterrupt as e:
        INTERFACES['mqtt<local>'].stop_thread()
        INTERFACES['mqtt<maestro>'].stop_thread()
        print(e)
    finally:
        sys.exit(exit_code)
