"""Cloud Manager to access Maestro"""
import os
import time
import threading
import sys
import json
import logging
import requests
import aiomqtt

log = logging.getLogger(__name__)

class CloudManager:
    """Cloud Manager to access Maestro"""
    def __init__(self,
                 dirs: dict,
                 interfaces: dict,
                 managers: dict,
                 drivers: dict
                ):
        log.debug('Initializing Cloud Manager.')

        self.dirs = dirs
        self.interfaces = interfaces
        self.managers = managers
        self.drivers = drivers
        self.login_to_maestro()
        log.info('Cloud Manager initialized.')

    def login_to_maestro(self):
        """Login to Maestro"""
        log.debug("Reaching Maestro Server")
        callback_topic = f"{self.interfaces['mqtt<maestro>'].client_id}/callback/cloud_manager"

        self.interfaces['mqtt<maestro>'].register_callback(
            "callback/cloud_manager",
            self.login_callback
            )

        self.interfaces['mqtt<maestro>'].publish(
            topic="maestro/login",
            payload=json.dumps({
                "client_id": self.interfaces['mqtt<maestro>'].client_id,
                "ip_address": requests.get(
                    'https://api.ipify.org?format=json', 
                    timeout=1).json()['ip'],
                "mqtt_topic": f"{self.interfaces['mqtt<maestro>'].client_id}/#",
                "callback": callback_topic
            })
        )
        log.debug("Connecting to Maestro Server")
        # Set a watchdog to closes the program in case the MQTT does not receive the callback
        # Start a timeout timer
        self.timeout_timer = threading.Timer(10.0, self.handle_timeout)  # Timeout in seconds
        self.timeout_timer.start()

    def handle_timeout(self):
        """Handle timeout for Maestro login"""
        log.critical("Login to Maestro timed out")
        sys.exit(1)

    def login_callback(self, client, userdata, msg):
        """Callback function for Maestro"""
        log.debug("Callback from Maestro")
        payload = json.loads(msg.payload)
        if payload['status'] == 'success':
            log.info("Logged in to Maestro")
            self.timeout_timer.cancel()  # Cancel the timeout timer since we got a response
        else:
            log.critical("Failed to login to Maestro")
            sys.exit(1)

    def maestro_ping_resp(self, client, userdata, msg):
        """Answers the Ping from Maestro"""
        log.debug("Maestro ping...")
        self.interfaces['mqtt<maestro>'].publish(
            topic=f'{self.interfaces['mqtt<maestro>'].client_id}/ping'
            
        )
