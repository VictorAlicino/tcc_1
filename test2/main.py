"""The main entry point for the application."""

import sys
import asyncio
from typing import Final
import initializers

# Python Version
"""Some features used in this project are only available in recent versions of Python."""
REQUIRED_PYTHON_VER: Final = (3, 12, 0)

# OS Supported
"""Nothing can prevent you from running this project on an unsupported OS, but it is not recommended."""
SUPPORTED_OS: Final = ["linux", "darwin", "win32"]

# Directories Path
"""This directories are used for the whole project as global viarables,
set them according to your system."""
DIRS: dict[str, str] = {
    "CORE": "core",
    "INTERFACES": "interfaces",
    "CONFIG": "config",
    "DRIVERS": "drivers",
    "DATABASES": "db",
    "SERVER": "server",
    "LOGS": "logs",
}

# GLobal Variables
"""This are the global variables that hold most of the objects shared between the modules."""
CONFIG: dict = {}       # Global Configuration
DRIVERS: dict = {}      # Drivers objects
INTERFACES: dict = {}   # Interfaces objects
MANAGERS: dict = {      # Managers
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
    initializers.define_log(DIRS, log_level= log_level) # Define the LOG modes and formatting
    initializers.check_python(REQUIRED_PYTHON_VER)      # Check the Python version
    initializers.check_os(SUPPORTED_OS)                 # Check the OS
    initializers.check_directories(DIRS)                # Check the directories
    CONFIG = initializers.load_configurations()         # Load the configurations
    # The initalizers order is: Database -> Interfaces -> Managers -> Drivers
    # DO NOT! load the initalizers in a different order unless you want to
    # see some nasty exceptions
    initializers.load_db(DIRS, INTERFACES)              # Load the database into INTERFACES['opus_db']
    initializers.load_interfaces(
        config=CONFIG,
        dirs=DIRS,
        interfaces=INTERFACES
    )
    initializers.load_managers(                         # Load the managers into MANAGERS['locations', 'devices', 'maestro' and 'users']
        dirs=DIRS,
        managers=MANAGERS,
        interfaces=INTERFACES,
        drivers=DRIVERS
    )
    initializers.load_drivers(                          # Load the drivers
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
        INTERFACES['mqtt<local>'].stop_thread()
        INTERFACES['mqtt<maestro>'].stop_thread()
        a.stop()
        print(e)
        sys.exit(127)
    except Exception as e:
        print(e)
    finally:
        sys.exit(exit_code)
