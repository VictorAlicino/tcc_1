"""Cloud Manager to access Maestro"""
import os
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

    def login_callback(self, client, userdata, msg):
        """Callback function for Maestro"""
        log.debug("Callback from Maestro")
        payload = json.loads(msg.payload)
        if payload['status'] == 'success':
            log.info("Logged in to Maestro")
        else:
            log.error("Failed to login to Maestro")
