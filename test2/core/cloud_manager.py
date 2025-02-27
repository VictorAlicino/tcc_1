"""Cloud Manager to access Maestro"""
import os
import time
import threading
import sys
import json
import logging
import requests
import aiomqtt
from db import crud
import db.models as models

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
        self.opus_db = interfaces['opus_db']
        self.login_to_maestro()
        self._configure_mqtt()
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

    def _configure_mqtt(self) -> None:
        """Configure MQTT"""
        log.debug('Configuring MQTT for Cloud Manager.')
        self.interfaces['mqtt<maestro>'].register_callback('cloud/#', self._mqtt_callback)
        self._mqtt_root_topic = f'{self.interfaces["mqtt<maestro>"].client_id}/cloud'
        log.debug('MQTT Configured for Cloud Manager.')

    def maestro_ping_resp(self, client, userdata, msg):
        """Answers the Ping from Maestro"""
        log.debug("Maestro ping...")
        self.interfaces['mqtt<maestro>'].publish(
            topic=f'{self.interfaces["mqtt<maestro>"].client_id}/ping'
        )

    def _get_user_full(self, payload: json) -> None:
        """Get all data including the devices from a user"""
        user = crud.get_user_by_id(self.opus_db.get_db(), payload['user_pk'])
        if not user:
            log.error("Maestro requested the full data of a user that does not exist")
            return
        log.debug(f"Maestro requested the full data of user {user.given_name}")

        user_data = {
            "user_pk": str(user.user_pk),
            "given_name": user.given_name,
            "email": user.email,
            "role": str(user.fk_role),
        }

        user_role = crud.get_role_uuid(self.opus_db.get_db(), user.fk_role)
        authorized_devices = crud.get_all_devices_authorized_to_a_role(self.opus_db.get_db(), user_role)

        authorized_devices_map = {str(device.device_pk): device for device in authorized_devices}

        buildings = next(self.opus_db.get_db()).query(models.Building).all()
        
        user_data["role"] = user_role.role_name

        response = {"buildings": []}

        for building in buildings:
            building_data = {
                "building_pk": str(building.building_pk),
                "security_level": user_role.role_name,
                "building_name": building.building_name,
                "spaces": []
            }

            for space in building.spaces:
                space_data = {
                    "building_space_pk": str(space.building_space_pk),
                    "space_name": space.space_name,
                    "rooms": []
                }

                for room in space.rooms:
                    room_data = {
                        "building_room_pk": str(room.building_room_pk),
                        "room_name": room.room_name,
                        "devices": []
                    }

                    for device in room.devices:
                        if str(device.device_pk) in authorized_devices_map:
                            room_data["devices"].append({
                                "device_pk": str(device.device_pk),
                                "device_name": device.device_name,
                                "device_type": device.device_type
                            })

                    space_data["rooms"].append(room_data)

                building_data["spaces"].append(space_data)

            response["buildings"].append(building_data)

        self.interfaces['mqtt<maestro>'].publish(
            topic=f'{payload["callback"]}',
            payload=json.dumps(response)
        )

    def _mqtt_callback(self, client, userdata, msg): # pylint: disable=unused-argument
        """Callback from MQTT when Maestro sends a message in the /cloud topic"""
        match msg.topic:
            case topic if topic == f'{self._mqtt_root_topic}/ping':
                self.maestro_ping_resp()
            case topic if topic == f'{self._mqtt_root_topic}/get_user_full':
                self._get_user_full(json.loads(msg.payload))
            case _:
                print("Message not recognized by the Cloud Manager")