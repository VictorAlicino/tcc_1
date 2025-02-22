"""Devices API Router."""

import logging
import db.users as maestro_users
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, status
from configurations.config import OpenConfig
from api.rest.localservers import router
from db.database import DB
from db.models import OpusServer, MaestroUser
from db import localservers as opus_servers
from api.mqtt import devices as MQTT_Devices
from api.rest.auth_conductor import oauth2_scheme
from api.rest.users import get_user_requesting

log = logging.getLogger(__name__)
config = OpenConfig()
db = DB()

router = APIRouter(
    prefix="/opus_server",
    tags=["Opus Server Devices"],
)

@router.get("/{server_id}/devices/{device_id}")
async def get_device_state(
    server_id: str,
    device_id: str,
    validate: str = Depends(oauth2_scheme),
    db_session=Depends(db.get_db)):
    """Get the state of a device."""
    # TODO: Add authentication
    local_server: OpusServer | None = opus_servers.get_server_by_id(db_session, server_id)
    if not local_server:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content="Server not found"
        )
    return await MQTT_Devices.get_device_state(local_server, device_id)

@router.put("/{server_id}/devices/{device_id}/set_state")
async def device_set_state(
    server_id: str,
    device_id: str,
    state: dict,
    validate: str = Depends(oauth2_scheme),
    db_session=Depends(db.get_db)):
    """Set the state of a device."""

    user: MaestroUser | None = get_user_requesting(validate, db_session)
    if not user:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content="User not found"
        )
    
    if server_id not in maestro_users.get_servers_of_user(db_session, user.user_id):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content="User not authorized to access this server"
        )
    
    local_server: OpusServer | None = opus_servers.get_server_by_id(db_session, server_id)
    if not local_server:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content="Server not found"
        )
    
    local_server_response = await MQTT_Devices.device_set_state(local_server, user, device_id, state)
    if not local_server_response:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="Internal server error"
        )
    print(local_server_response)
    match local_server_response['status']:
        case 'sucess':
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=local_server_response['reason']
            )
        case 'failed':
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=local_server_response['reason']
            )
    