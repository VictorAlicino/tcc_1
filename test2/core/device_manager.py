"""Devices Manager"""
import os
import logging
from .devices import hvac, light

log = logging.getLogger(__name__)


class DeviceManager:
    """Devices Manager"""

    def __init__(self, dirs: dict, interfaces: dict):
        log.debug('Initializing Device Manager.')
        self.devices: dict = {}  # This is gonna be hella big
        self.available_devices: dict = {}  # This is gonna be worse
        self.opus_db = interfaces['opus_db']

        self._manager_init(dirs)
        log.debug('Device Manager initialized.')

    def _manager_init(self, dirs: dict) -> None:
        """Initialize Device Manager in-memory database"""
        log.debug('Initializing Device Manager in-memory database.')
        for device_type in os.listdir(f'{dirs['CORE']}/devices'):
            if device_type.endswith('.py') and not device_type.startswith('__'):
                log.debug('Creating virtual db for %s', device_type[:-3])
                self.devices[f'opus_{device_type[:-3]}'] = {}
        log.debug('Device Manager in-memory database initialized.')

    def new_device(self, device) -> None:
        """Add a new device to available devices"""
        log.debug('Adding new available device.')
        if f'{device.driver}' not in self.available_devices:
            self.available_devices[f'{device.driver}'] = []
        self.available_devices[f'{device.driver}'].append(device)
        log.debug('└── New Device Available %s',
                  device)
        log.debug('   ├── Device Type: OpusLight')
        log.debug('   └── Device Driver: %s', device.driver)

    def register_device(self, device) -> None:
        """Register a device in the device manager"""
        log.debug('Adding device %s | %s to the device manager.',
                  device.__class__, device)
        # c = self.db_conn.cursor()
        if isinstance(device, light.OpusLight):
            log.debug('Adding light %s to the device manager.',
                      device.name)
            # self.devices['light'].append(device)
            # Add to the database
            # c.execute('INSERT INTO device (name, type) VALUES (?, ?)', (device.name, 'light'))
        if isinstance(device, hvac.OpusHVAC):
            self.devices['hvac'].append(device)

    def get_available_devices(self) -> list:
        """Return all available devices"""
        return self.available_devices

    def print_all_devices(self) -> None:
        """Print all devices"""
        log.debug('All devices in the device manager')
        log.debug('├──REGISTERED DEVICES')
        for device_type, devices in self.devices.items():
            log.debug('│\t├── %s: %s', device_type, devices)
        log.debug('│\t└── END OF REGISTERED DEVICES')
        log.debug('└──AVAILABLE DEVICES')
        for device_type, devices in self.available_devices.items():
            log.debug('\t├── %s', device_type)
            for device in devices:
                log.debug('\t│\t├── %s', device)
            log.debug('\t│\t└── END OF %s', device_type)
        log.debug('\t└── END OF AVAILABLE DEVICES')
