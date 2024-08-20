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
    if len(sys.argv) >= 2:
        log_level = sys.argv[1]
    else:
        log_level = "INFO"
    initializers.define_log(DIRS, log_level= log_level)
    initializers.check_python(REQUIRED_PYTHON_VER)
    initializers.check_os(SUPPORTED_OS)
    initializers.check_directories(DIRS)
    CONFIG = initializers.load_configurations()
    # The initalizers order is: Database -> Interfaces -> Managers -> Drivers
    # DO NOT! load the initalizers in a different order unless you want to
    # see some nasty exceptions
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
    a: asyncio.AbstractEventLoop
    try:
        a = asyncio.run(main())
    except KeyboardInterrupt as e:
        sys.exit(127)
        INTERFACES['mqtt<local>'].stop_thread()
        INTERFACES['mqtt<maestro>'].stop_thread()
        a.stop()
        print(e)
    except Exception as e:
        print(e)
    finally:
        sys.exit(exit_code)
