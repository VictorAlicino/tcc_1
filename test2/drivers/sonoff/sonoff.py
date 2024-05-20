"""SONOFF Connection Driver"""
import logging
from ipaddress import ip_address
# Non-Standard Libraries
import json
from uuid import UUID, uuid1
from zeroconf import ServiceBrowser, Zeroconf
from core.device_manager import DeviceManager
from core.devices.__generic import DeviceType
from .sonoff_device import SonoffDevice
from .sonoff_light import SonoffLight

log = logging.getLogger(__name__)

interfaces: dict[any, str] = {}

OPUS_D_MANAGER: DeviceManager = None

def _found_new_device(name, info) -> None:
    ip = info.addresses[0]
    new_device = SonoffDevice(ip_address(f'{ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}'))
    new_device.id = uuid1()
    new_device.hostname = name.split('.')[0]
    new_device.port = info.port
    new_device.bssid = None
    new_device.device_type = bytes(info.properties[('type').encode('utf-8')]).decode()
    new_device.service_instace_name = info.type
    new_device.device_id = bytes(info.properties[('id').encode('utf-8')]).decode()
    new_device.startup_info_dump = info.properties

    match info.properties.get(b'type'):
        case b'diy_plug':
            new_device.type = DeviceType.LIGHT
        case b'diy_meter':
            new_device.type = "SONOFF_METER"
        case _:
            new_device.type = DeviceType.UNKNOWN

    # Check if the device is already registered
    try:
        for device_type in OPUS_D_MANAGER.devices:
            for device in OPUS_D_MANAGER.devices[device_type].values():
                if device.driver == 'sonoff' and device.device_id == new_device.device_id:
                    log.warning("Device already registered: %s", new_device.device_id)
                    return
    except KeyError:
        ...
    # Check if the device is already available
    try:
        for device in OPUS_D_MANAGER.available_devices['sonoff']:
            if device.device_id == new_device.device_id:
                log.warning("Device already available: %s", new_device.device_id)
                return
    except KeyError:
        ...

    OPUS_D_MANAGER.new_device(new_device)

sonoff_discovered_devices: list = []

class MDNSListener:
    """Listener for Sonoff mDNS Service"""

    def remove_service(self, zeroconf, type, name): # pylint: disable=redefined-builtin
        """"Remove Service"""
        # do nothing

    def update_service(self, zeroconf, type, name): # pylint: disable=redefined-builtin, unused-argument
        """Update Service"""
        #print(f'Update Service {name} {type}')
        info = zeroconf.get_service_info(type, name)
        if info:
            #if (info.properties.get(b'id').decode() in
            #[device.device_id for device in OPUS_D_MANAGER.available_devices['sonoff']]):
            #    log.debug("Device %s state changed -> %s",
            #              info.properties.get(b'id').decode(),
            #              info.properties)
            log.debug("Device %s state changed -> %s",
                      info.properties.get(b'id').decode(),
                      info.properties)

    def add_service(self, zeroconf, type, name): # pylint: disable=redefined-builtin
        """Add a Device to the known devices list"""
        info = zeroconf.get_service_info(type, name)
        # If info is not None and the device is not encrypted
        if info and info.properties.get(b'encrypt') is None:
            _found_new_device(name, info)

def start_sonoff_finder() -> None:
    """Search for Sonoff Devices in the network"""
    zeroconf = Zeroconf()
    listener = MDNSListener()
    ServiceBrowser(zeroconf, "_ewelink._tcp.local.", listener)

def new_light(name: str, base_device: SonoffDevice) -> SonoffLight:
    """Create a new Sonoff Light"""
    log.debug("Registering new Sonoff Light: %s", name)
    new = SonoffLight(name, base_device)
    return new

def load_light(name: str, driver_data: dict) -> SonoffLight:
    """Load a Sonoff Light"""
    log.debug("Loading Sonoff Light: %s", name)
    temp_obj = SonoffDevice(ip_address(driver_data['ip_address']))
    temp_obj.id = UUID(driver_data['id'])
    temp_obj.hostname = driver_data['hostname']
    temp_obj.port = driver_data['port']
    temp_obj.bssid = driver_data['bssid']
    temp_obj.device_type = driver_data['device_type']
    temp_obj.device_id = driver_data['device_id']
    temp_obj.startup_info_dump = driver_data['startup_info_dump']
    new = SonoffLight(name, temp_obj)
    return new

def start(dirs: dict,
          config: dict,
          drivers: dict,
          interfaces: dict,
          managers: dict) -> None:
    """Main Function"""
    log.debug("Starting Sonoff Driver")
    global OPUS_D_MANAGER # pylint: disable=global-statement
    OPUS_D_MANAGER = managers['devices']
    start_sonoff_finder()
