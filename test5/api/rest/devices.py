"""Devices API Router."""

import logging
import db.users as maestro_users
import os
from datetime import datetime, timedelta
from dataclasses import dataclass
from jose import JWTError, jwt
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import APIRouter, Depends, Request, status
from configurations.config import OpenConfig
from api.rest.localservers import router
from db.database import DB
from db.models import OpusServer, MaestroUser
from db import localservers as opus_servers
from api.mqtt import devices as MQTT_Devices
from api.rest.auth_conductor import oauth2_scheme
from api.rest.users import get_user_requesting
import utils.qr_code_generator as qr_code_generator

log = logging.getLogger(__name__)
config = OpenConfig()
db = DB()

# Current user on guest access to a device
"""
{
    "server_id": {
        "device_id": 
            {
                "current_guest": "user_id",
                "granted_until": "timestamp"
            }
    }
}
"""
guest_users_devices: dict[str, dict[str, dict[str, str]]] = {}

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
        # Check if the user is authorized to be a guest
        try:
            curr_guest_user = guest_users_devices[server_id][device_id]['current_guest']
            if curr_guest_user != user.user_id: 
                raise KeyError
        except KeyError:
            log.warning(f"User Mr(s). {user.family_name} is not authorized to set state of device {device_id} on server {server_id}")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content="User not authorized to set state of device"
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
    
@router.get("/qr_code/{server_id}/{device_id}")
async def get_guest_acess_qr_code(
    request: Request,
    server_id: str,
    device_id: str,
    validate: str = Depends(oauth2_scheme),
    db_session=Depends(db.get_db)):
    """Get the QR code for guest access."""
    base_url = str(request.base_url)
    user: MaestroUser | None = get_user_requesting(validate, db_session)
    if user is None:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content="User not found or not authorized"
        )
    server_admins = {admin[0] for admin in opus_servers.get_server_admins(db_session, server_id)}
    if str(user.user_id) not in server_admins:
        log.warning(f"User ({user.email}) is not authorized request a QR code for guest access to device {device_id} on server {server_id}")
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content="User not authorized to get guest access to device"
        )
    log.debug(f"User {user.given_name} ({user.email}) is requesting a QR code for guest access to device {device_id} on server {server_id}")
    if(os.path.exists(f"qr_codes/{server_id}/{device_id}.png")):
        path = f"qr_codes/{server_id}/{device_id}.png"
        return RedirectResponse(url=f"{base_url}/assetes/{path}", status_code=status.HTTP_201_CREATED)
    else:
        path = qr_code_generator.generate_guest_acess(server_id, device_id)
        return RedirectResponse(url=f"{base_url}{path}", status_code=status.HTTP_302_FOUND)
    
@router.get("/guest_access/{cypher_text}")
async def get_guest_access(
    cypher_text: str,
    validate: str = Depends(oauth2_scheme),
    db_session=Depends(db.get_db)):
    """Get the guest access information."""
    try:
        cypher_suite = jwt.decode(cypher_text, config['api-secrets']['secret_key'], algorithms=["HS256"])
    except JWTError:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="Invalid cypher text"
        )
    local_server = opus_servers.get_server_by_id(db_session, cypher_suite['server_id'])
    user = get_user_requesting(validate, db_session)

    if not local_server:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content="Server not found"
        )
    
    if not user:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content="User not found"
        )
    
    global guest_users_devices
    
    guest_users_devices.setdefault(cypher_suite['server_id'], {})
    guest_users_devices[cypher_suite['server_id']].setdefault(cypher_suite['device_id'], {"current_guest": None, "granted_until": None})

    # Get the current guest user, time expired or not
    current_guest: str = guest_users_devices[cypher_suite['server_id']][cypher_suite['device_id']]['current_guest'] 

    if current_guest != user.user_id: # If it's a new guest user
        guest_users_devices[cypher_suite['server_id']][cypher_suite['device_id']]['current_guest'] = user.user_id
        granted_until = (datetime.now() + timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S")
        guest_users_devices[cypher_suite['server_id']][cypher_suite['device_id']]['granted_until'] = granted_until
        log.debug(f"User {user.user_id} has been granted GUEST access to device {cypher_suite['device_id']} on server {cypher_suite['server_id']} until {granted_until}")
    else: # If the guest user is the same as before, maybe to refresh the time
        granted_until = guest_users_devices[cypher_suite['server_id']][cypher_suite['device_id']]['granted_until']
        log.debug(f"User {user.user_id} already has GUEST access to device {cypher_suite['device_id']} on server {cypher_suite['server_id']} until {granted_until}")
        if datetime(granted_until) < datetime.now():
            granted_until = (datetime.now() + timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S")
            guest_users_devices[cypher_suite['server_id']][cypher_suite['device_id']]['granted_until'] = granted_until
            log.debug(f"User {user.user_id} has refreshed GUEST access to device {cypher_suite['device_id']} on server {cypher_suite['server_id']} until {granted_until}")

    device = await MQTT_Devices.get_device(local_server, cypher_suite['device_id'])
    device_state = await MQTT_Devices.get_device_state(local_server, cypher_suite['device_id'])
    device_type = await MQTT_Devices.get_device_type(local_server, cypher_suite['device_id'])
    response = {
        "server_id": cypher_suite['server_id'],
        "grant_until": granted_until,
        "device": device,
        "state": device_state
    }
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=response
    )
