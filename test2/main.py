"""The main entry point for the application."""

import sys
import os
import asyncio
import importlib
from types import ModuleType
from typing import Final
import yaml

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


def check_configurations() -> None:
    """Check if the configurations are valid."""
    print("Checking configurations...")

    # Check the YAML files
    print("Checking YAML files...")
    for file in os.listdir(DIRS["CONFIG"]):
        if file.endswith(".yaml"):
            print(f"Found: {file}")


def check_os() -> None:
    """Check if the right OS is running."""
    print("Checking OS...")
    print(f"OS: {sys.platform}")

    is_supported: bool = False
    for os_name in SUPPORTED_OS:
        if sys.platform == os_name:
            is_supported = True
            break
    if is_supported is False:
        print(f"{sys.platform} is currentely not supported.")
        sys.exit(1)


def check_python() -> None:
    """Check if the right Python version is running."""
    print("Checking Python version...")
    print(f"Python version: {sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}")
    if sys.version_info < REQUIRED_PYTHON_VER:
        print(f"ERROR: Python {REQUIRED_PYTHON_VER[0]}."
              f"{REQUIRED_PYTHON_VER[1]}."
              f"{REQUIRED_PYTHON_VER[2]} "
              f"or higher is required.")
        sys.exit(1)

def check_directories() -> None:
    """Check if all the required directories exist."""
    print("Checking directories...")
    for directory in DIRS.items():
        print(f"Checking for {directory[0]}...", end=" ")
        if not os.path.exists(f"./{directory[1]}") and not os.path.isdir(f"./{directory[1]}"):
            print(f"ERROR: {directory[1]} directory does not exist.")
            sys.exit(1)
        print(f"Found at ./{directory[1]}")

def load_configurations() -> None:
    """Load the config file into the CONFIG global variable."""
    print("Loading configurations...")
    global CONFIG # pylint: disable=global-statement
    with open("./config/config.yaml", "r", encoding='utf-8') as file:
        CONFIG = yaml.load(file, Loader=yaml.FullLoader)
    print("Configurations loaded.")

def load_interfaces() -> None:
    """This function uses the importlib module to load the interfaces."""
    print("Loading interfaces...")
    interfaces_list: list = CONFIG["interfaces"]

    for interface_name in interfaces_list:
        print(f"Looking for {interface_name} interface...")
        #for file in os.listdir(f'./{DIRS["INTERFACES"]}/{interface_name}'):
        #    if file == "__init__.py":
        #        # Importing Interface (a.k.a Python Module)
        #        global INTERFACES # pylint: disable=global-variable-not-assigned
        #        print('Found')
        #        INTERFACES[interface_name] = importlib.import_module(
        #            f"{DIRS["INTERFACES"]}.{interface_name}.{interface_name}"
        #            )
        #        print(f"Imported <<{interface_name}>> interface")

def load_drivers() -> None:
    """This function uses the importlib module to load the drivers."""
    print("Loading drivers...")
    drivers_list: list = CONFIG["drivers"]

    for driver_name in drivers_list:
        print(f"Looking for {driver_name} driver...", end=" ")
        for file in os.listdir(f'./{DIRS["DRIVERS"]}/{driver_name}'):
            if file == "__init__.py":
                # Importing Driver (a.k.a Python Module)
                global DRIVERS # pylint: disable=global-variable-not-assigned
                print('Found')
                DRIVERS[driver_name] = importlib.import_module(
                    f"{DIRS["DRIVERS"]}.{driver_name}.{driver_name}"
                    )
                print(f"Imported <<{driver_name}>> driver")


async def main() -> None:
    """The main function."""
    await DRIVERS['sonoff'].start()
    await asyncio.sleep(2)
    print(DRIVERS['sonoff'].get_registered_devices())
    luz1 = await DRIVERS['sonoff'].create_sonoff_light(
        "Luz1",
        DRIVERS['sonoff'].get_known_devices()[0]
        )
    while True:
    #    try:
    #        await luz1.on()
    #        await asyncio.sleep(1)
    #        await luz1.off()
    #        await asyncio.sleep(1)
    #    except KeyboardInterrupt as exp1:
    #        print(f"{exp1} Interrupted by user")
    #        break
        ...


if __name__ == "__main__":
    exit_code: int = 0

    check_python()
    check_os()
    check_directories()
    load_configurations()
    load_interfaces()
    load_drivers()
    # TODO: Start devices manager

    # TODO: Connect to database
    # TODO: Start event manager
    # TODO: Start task manager


    #try:
    #    asyncio.run(main())
    #except KeyboardInterrupt as e:
    #    print(e)
    sys.exit(exit_code)
