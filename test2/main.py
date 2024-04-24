"""The main entry point for the application."""

import sys
import os
import asyncio
import importlib
from typing import Final
import yaml

# Python Version
REQUIRED_PYTHON_VER: Final = (3, 12, 0)

# OS Supported
SUPPORTED_OS: Final = ["linux", "darwin", "win32"]

# Global Configuration
CONFIG: dict = {}


def check_configurations() -> None:
    """Check if the configurations are valid."""
    print("Checking configurations...")
    config_folder = "./configurations"

    # Check if the configurations folder exists
    if not os.path.exists(config_folder) and not os.path.isdir(config_folder):
        print("ERROR: Configurations folder does not exist.")
        sys.exit(1)
    print(f"Configurations Folder found at {config_folder}")

    # Check the YAML files
    print("Checking YAML files...")
    for file in os.listdir(config_folder):
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


def load_configurations() -> None:
    """Load the config file into the CONFIG global variable."""
    print("Loading configurations...")
    if not os.path.exists("./config") and not os.path.isdir("./config"):
        print("ERROR: Configurations folder does not exist.")
        sys.exit(1)
    global CONFIG # pylint: disable=global-statement
    with open("./config/config.yaml", "r", encoding='utf-8') as file:
        CONFIG = yaml.load(file, Loader=yaml.FullLoader)
    print("Configurations loaded.")


def load_drivers() -> None:
    """This function uses the importlib module to load the drivers."""
    print("Loading drivers...")
    drivers_folder = "drivers"
    if not os.path.exists(f'./{drivers_folder}') and not os.path.isdir(f'./{drivers_folder}'):
        print("ERROR: Drivers folder does not exist.")
        sys.exit(1)
    print(f"Drivers found at ./{drivers_folder}")
    drivers_list: list = CONFIG["drivers"]

    for driver_name in drivers_list:
        print(f"Looking for {driver_name} driver...", end=" ")
        for file in os.listdir(f'./{drivers_folder}/{driver_name}'):
            if file == "__init__.py":
                # Importing Driver (a.k.a Python Module)
                print('Found')
                print(f"Importing <<{driver_name}>> driver")
                globals()["sonoff"] = importlib.import_module(f"{drivers_folder}.{driver_name}")
                print(sys.modules.keys())


async def main() -> None:
    """The main function."""
    while True:
        ...

if __name__ == "__main__":
    exit_code: int = 0

    check_python()
    check_os()
    load_configurations()
    load_drivers()
    # TODO: Connect to database
    # TODO: Start entity manager
    # TODO: Start event manager
    # TODO: Start task manager

    asyncio.run(main())
    sys.exit(exit_code)
