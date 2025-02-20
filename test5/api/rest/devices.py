"""Devices API Router."""

import logging
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, status
from configurations.config import OpenConfig
from api.rest.localservers import router
from db.database import DB
from db.models import OpusServer
from db import localservers as opus_servers
from api.mqtt import devices as MQTT_Devices
from api.rest.auth_conductor import oauth2_scheme

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
