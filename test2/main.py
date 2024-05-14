"""The main entry point for the application."""

import sys
import os
import asyncio
import importlib
import logging
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


def define_log() -> None:
    """Logging System"""
    logging.basicConfig(encoding='utf-8', level=logging.DEBUG,
                            format=
                            #'[%(levelname)s][%(filename)s:%(lineno)d][%(name)s] %(message)s', # pylint: disable=line-too-long
                            '%(filename)s -> %(message)s',
                            handlers=[
                                #logging.FileHandler("debug.log"),
                                logging.StreamHandler()
                            ]
                            )


def check_configurations() -> None:
    """Check if the configurations are valid."""
    logging.debug("Checking configurations...")

    # Check the YAML files
    logging.debug("Checking YAML files...")
    for file in os.listdir(DIRS["CONFIG"]):
        if file.endswith(".yaml"):
            logging.debug("Found: %(file)s")


def check_os() -> None:
    """Check if the right OS is running."""
    logging.debug("Checking OS...")
    logging.debug("OS: %s", sys.platform)

    is_supported: bool = False
    for os_name in SUPPORTED_OS:
        if sys.platform == os_name:
            is_supported = True
            break
    if is_supported is False:
        logging.error("%s is currentely not supported.", sys.platform)
        sys.exit(1)


def check_python() -> None:
    """Check if the right Python version is running."""
    logging.debug("Checking Python version...")
    logging.debug("Python version: %d.%d.%d",
                  sys.version_info[0],sys.version_info[1],sys.version_info[2])
    if sys.version_info < REQUIRED_PYTHON_VER:
        logging.error("Python %d.%d.%d or higher is required.", REQUIRED_PYTHON_VER[0],
                      REQUIRED_PYTHON_VER[1], REQUIRED_PYTHON_VER[2])
        sys.exit(1)


def check_directories() -> None:
    """Check if all the required directories exist."""
    logging.debug("Checking directories...")
    for directory in DIRS.items():
        if not os.path.exists(f"./{directory[1]}") and not os.path.isdir(f"./{directory[1]}"):
            logging.error("%s directory does not exist.", directory[1])
            sys.exit(1)
        logging.debug("%s found at ./%s", directory[0], directory[1])


def load_configurations() -> None:
    """Load the config file into the CONFIG global variable."""
    logging.debug("Loading configurations...")
    global CONFIG # pylint: disable=global-statement
    with open("./config/config.yaml", "r", encoding='utf-8') as file:
        CONFIG = yaml.load(file, Loader=yaml.FullLoader)
    logging.debug("Configurations loaded.")


def load_interfaces() -> None:
    """This function uses the importlib module to load the interfaces."""
    logging.debug("Loading interfaces...")

    # To each interface found in the interfaces directory
    for file in os.listdir(f'./{DIRS["INTERFACES"]}'):
        if file == "__init__.py":
            continue
        # Compare against the expected interfaces in the config file
        for interface in CONFIG["interfaces"]:
            try:
                # For each interface NAME in the config file
                for interface_name in interface.keys():
                    # If the interface file is found
                    if file == f"{interface_name}.py":
                        # Import the interface module
                        interface_module = importlib.import_module(
                            f"{DIRS['INTERFACES']}.{interface_name}"
                            )
                        # and load the interface class
                        INTERFACES[interface_name] = interface_module.initialize()
                        # Initialize the interface with the config
                        rs = INTERFACES[interface_name].begin(interface[interface_name])
                        if rs is False:
                            logging.error("Could not initialize %s interface",
                                          interface_name)
                            sys.exit(1)
                        logging.info("Added [%s] interface", interface_name)
            except AttributeError:
                logging.error("YAML file is not properly formatted")
                sys.exit(1)


def load_drivers() -> None:
    """This function uses the importlib module to load the drivers."""
    logging.debug("Loading drivers...")
    drivers_list: list = CONFIG["drivers"]

    for driver_name in drivers_list:
        logging.debug("Looking for <<%s>> driver...", driver_name)
        for file in os.listdir(f'./{DIRS["DRIVERS"]}/{driver_name}'):
            if file == "__init__.py":
                # Importing Driver (a.k.a Python Module)
                global DRIVERS # pylint: disable=global-variable-not-assigned
                logging.debug("Importing <<%s>> driver...", driver_name)
                DRIVERS[driver_name] = importlib.import_module(
                    f"{DIRS['DRIVERS']}.{driver_name}.{driver_name}"
                    )
                for interface in DRIVERS[driver_name].interfaces:
                    if interface not in INTERFACES:
                        logging.error("Interface [%s] is required for <<%s>> driver",
                                      interface, driver_name)
                        sys.exit(1)
                    else:
                        DRIVERS[driver_name].interfaces[interface] = INTERFACES[interface]
                        logging.info("Interface [%s] synced with <<%s>> driver",
                                     interface, driver_name)
                logging.info("Imported <<%s>> driver", driver_name)


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

    define_log()
    check_python()
    check_os()
    check_directories()
    load_configurations()
    load_interfaces()
    #print(INTERFACES)
    load_drivers()
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
