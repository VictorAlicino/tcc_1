"""Devices Manager"""
import os
import sqlite3
import logging
from .devices import hvac, light

log = logging.getLogger(__name__)

class DeviceManager():
    """Devices Manager"""

    def __init__(self, dirs: dict):
        log.debug('Initializing Device Manager.')
        self.devices: dict = {}  # This is gonna be hella big
        self.available_devices: dict = {} # This is gonna be worse

        log.debug('Connecting to the local database.')
        self.db_conn = sqlite3.connect(f'{dirs['DATABASES']}/opus-vault.db') # Persistent database
        with open(f'{dirs['DATABASES']}/create_db.sql', 'r', encoding='utf-8') as f:
            c = self.db_conn.cursor()
            c.executescript(f.read())

        self._manager_init(dirs)
        log.debug('Device Manager initialized.')


    def _manager_init(self, dirs: dict) -> None:
        """Initialize Device Manager in-memory database"""
        log.debug('Initializing Device Manager in-memory database.')
        for device_type in os.listdir(f'{dirs['CORE']}/devices'):
            if device_type.endswith('.py') and not device_type.startswith('__'):
                log.debug('Creating virtual db for %s', device_type[:-3])
                self.devices[f'opus_{device_type[:-3]}'] = {}
                self.available_devices[f'opus_{device_type[:-3]}'] = {}
        log.debug('Device Manager in-memory database initialized.')


    def new_device(self, device) -> None:
        """Add a new device to available devices"""
        log.debug('Adding new available device.')
        log.debug('├──Device Name: %s', device.name)
        if isinstance(device, light.OpusLight):
            log.debug('├──Device Type: OpusLight')
            log.debug('└──Device Driver: %s', device.driver)
            self.available_devices['opus_light'][device.name] = device
        if isinstance(device, hvac.OpusHVAC):
            log.debug('├──Device Type: OpusHVAC')
            log.debug('└──Device Driver: %s', device.driver)
            self.available_devices['opus_hvac'][device.name] = device


    def register_device(self, device) -> None:
        """Register a device in the device manager"""
        print(f'Adding device {device.__class__} to the device manager.')
        # c = self.db_conn.cursor()
        if isinstance(device, light.OpusLight):
            print(f'Adding light {device.name} to the device manager.')
            #self.devices['light'].append(device)
            # Add to the database
            # c.execute('INSERT INTO device (name, type) VALUES (?, ?)', (device.name, 'light'))
        if isinstance(device, hvac.OpusHVAC):
            self.devices['hvac'].append(device)

    def print_all_devices(self) -> None:
        """Print all devices"""
        log.debug('All devices in the device manager')
        log.debug('├──REGISTERED DEVICES')
        for device_type, devices in self.devices.items():
            log.debug('│\t├──%s: %s', device_type, devices)
        log.debug('│\t└── END OF REGISTERED DEVICES')
        log.debug('└──AVAILABLE DEVICES')
        for device_type, devices in self.available_devices.items():
            log.debug('\t├──%s: %s', device_type, devices)
        log.debug('\t└── END OF AVAILABLE DEVICES')
