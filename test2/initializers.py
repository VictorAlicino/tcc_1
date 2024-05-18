"""Initializers Module"""
import re
import sys
import os
import importlib
import logging
import yaml
from core.device_manager import DeviceManager
from core.location_manager import LocationManager
from db.db import OpusDB


def define_log() -> None:
    """Logging System"""
    logging.basicConfig(encoding='utf-8', level=logging.DEBUG,
                        format=
                        '[%(levelname)s][%(filename)s:%(lineno)d][%(name)s] %(message)s',
                        # '%(filename)s -> %(message)s',
                        handlers=[
                            # logging.FileHandler("debug.log"),
                            logging.StreamHandler()
                        ]
                        )

def check_configurations(dirs: dict) -> None:
    """Check if the configurations are valid."""
    logging.debug("Checking configurations...")

    # Check the YAML files
    logging.debug("Checking YAML files...")
    for file in os.listdir(dirs["CONFIG"]):
        if file.endswith(".yaml"):
            logging.debug("Found: %(file)s")

def check_os(supported_os: list) -> None:
    """Check if the right OS is running."""
    logging.debug("Checking OS...")
    logging.debug("OS: %s", sys.platform)

    is_supported: bool = False
    for os_name in supported_os:
        if sys.platform == os_name:
            is_supported = True
            break
    if is_supported is False:
        logging.error("%s is currently not supported.", sys.platform)
        sys.exit(1)

def check_python(required_python_ver: tuple) -> None:
    """Check if the right Python version is running."""
    logging.debug("Checking Python version...")
    logging.debug("Python version: %d.%d.%d",
                  sys.version_info[0], sys.version_info[1], sys.version_info[2])
    if sys.version_info < required_python_ver:
        logging.error("Python %d.%d.%d or higher is required.", required_python_ver[0],
                      required_python_ver[1], required_python_ver[2])
        sys.exit(1)

def check_directories(dirs: dict) -> None:
    """Check if all the required directories exist."""
    logging.debug("Checking directories...")
    for directory in dirs.items():
        if not os.path.exists(f"./{directory[1]}") and not os.path.isdir(f"./{directory[1]}"):
            logging.error("%s directory does not exist.", directory[1])
            sys.exit(1)
        logging.debug("%s found at ./%s", directory[0], directory[1])

def load_configurations() -> dict[str]:
    """Load the config file into and returns the reading."""
    logging.debug("Loading configurations...")
    with open("./config/config.yaml", "r", encoding='utf-8') as file:
        temp = yaml.load(file, Loader=yaml.FullLoader)
    logging.debug("Configurations loaded.")
    return temp

def load_db(dirs: dict, interfaces: dict) -> None:
    """Load the database."""
    logging.debug("Initializing database...")
    interfaces['opus_db'] = OpusDB(dirs["DATABASES"])
    logging.debug("Initializing loaded.")

def load_managers(dirs: dict, managers: dict, interfaces: dict) -> None:
    """This function loads the managers."""
    logging.debug("Loading managers...")
    managers["devices"] = DeviceManager(dirs, interfaces)
    managers["locations"] = LocationManager(interfaces)

def load_interfaces(config: dict, dirs: dict, interfaces: dict) -> None:
    """This function uses the importlib module to load the interfaces."""
    logging.debug("Loading interfaces...")

    # To each interface found in the interfaces directory
    for file in os.listdir(f'./{dirs["INTERFACES"]}'):
        if file == "__init__.py":
            continue
        # Compare against the expected interfaces in the config file
        for interface_config in config["interfaces"]:
            try:
                # For each interface NAME in the config file
                for interface_full_name in interface_config.keys():
                    interface_name = re.sub(r'<.*?>', '', interface_full_name)
                    # If the interface file is found
                    if file == f"{interface_name}.py":
                        # Import the interface module
                        interface_module = importlib.import_module(
                            f"{dirs['INTERFACES']}.{interface_name}"
                        )
                        # and load the interface class
                        interfaces[interface_full_name] = interface_module.initialize()
                        # Initialize the interface with the config
                        rs = interfaces[interface_full_name].begin(
                            interface_config[interface_full_name]
                            )
                        if rs is False:
                            logging.error("Could not initialize %s interface",
                                          interface_full_name)
                            sys.exit(1)
                        logging.info("Added [%s] interface", interface_full_name)
            except AttributeError:
                logging.error("YAML file is not properly formatted")
                sys.exit(1)


def load_drivers(config: dict,
                 dirs: dict,
                 interfaces: dict,
                 drivers: dict,
                 managers: dict) -> None:
    """This function uses the importlib module to load the drivers."""
    logging.debug("Loading drivers...")
    drivers_list: list = config["drivers"]

    for driver_name in drivers_list:
        logging.debug("Looking for <<%s>> driver...", driver_name)
        for file in os.listdir(f'./{dirs["DRIVERS"]}/{driver_name}'):
            if file == "__init__.py":
                # Importing Driver (a.k.a Python Module)
                logging.debug("Importing <<%s>> driver...", driver_name)
                drivers[driver_name] = importlib.import_module(
                    f"{dirs['DRIVERS']}.{driver_name}.{driver_name}"
                )
                for interface in drivers[driver_name].interfaces:
                    if interface not in interfaces:
                        logging.error("Interface [%s] is required for <<%s>> driver",
                                      interface, driver_name)
                        sys.exit(1)
                    else:
                        drivers[driver_name].interfaces[interface] = interfaces[interface]
                        logging.info("Interface [%s] synced with <<%s>> driver",
                                     interface, driver_name)
                drivers[driver_name].start(
                    dirs=dirs,
                    config=config,
                    drivers=drivers,
                    interfaces=interfaces,
                    managers=managers
                )
                logging.info("Imported <<%s>> driver", driver_name)
