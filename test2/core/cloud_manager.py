"""Cloud Manager to access Maestro"""
import os
import time
from threading import Thread
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
        self.watchdog_flag: bool = False;

        self.dirs = dirs
        self.interfaces = interfaces
        self.managers = managers
        self.drivers = drivers
        self.login_to_maestro()
        log.info('Cloud Manager initialized.')

    def cloud_watchdog(self, timeout_s: float = 10.0, fail_reason: str = "Watchdog timeout"):
        """Raise an exception if timeout exceeds the value on timeout"""
        target_time = time.time() + timeout_s;
        print(self.cloud_watchdog)
        def timer():
            print(self.cloud_watchdog)
            while self.watchdog_flag is False:
                print(self.cloud_watchdog)
                if time.time() >= target_time:
                    log.critical(fail_reason)
                    raise RuntimeError(fail_reason)
                time.sleep(0.1)  # Pequeno intervalo para evitar loop apertado
            self.watchdog_flag = False
        temp_thread = Thread(target=timer)
        temp_thread.start()

    def login_to_maestro(self):
        """Login to Maestro"""
        log.debug("Reaching Maestro Server")
        callback_topic = f"{self.interfaces['mqtt<maestro>'].client_id}/callback/cloud_manager"

        self.interfaces['mqtt<maestro>'].register_callback(
            callback_topic,
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
        self.cloud_watchdog(timeout_s=10, fail_reason="Maestro Server is not accessible")

    def login_callback(self, client, userdata, msg):
        """Callback function for Maestro"""
        log.debug("Callback from Maestro")
        payload = json.loads(msg.payload)
        if payload['status'] == 'success':
            log.info("Logged in to Maestro")
            self.cloud_watchdog = True
        else:
            log.error("Failed to login to Maestro")
            sys.exit(1);

    def maestro_ping_resp(self, client, userdata, msg):
        """Answers the Ping from Maestro"""
        log.debug("Maestro ping...")
        self.interfaces['mqtt<maestro>'].publish(
            topic=f'{self.interfaces['mqtt<maestro>'].client_id}/ping'
            
        )
        
