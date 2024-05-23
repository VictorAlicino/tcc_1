"""API endpoints for the server."""
import sys
import os
import json
import uvicorn
import yaml
from fastapi import FastAPI
from aiomqtt import Client
from models import Building, Space, Room, Device, DeviceByDriver, Command

if sys.platform.lower() == "win32" or os.name.lower() == "nt":
    from asyncio import set_event_loop_policy, WindowsSelectorEventLoopPolicy
    set_event_loop_policy(WindowsSelectorEventLoopPolicy())

# Load YAML file
with open("config.yaml", "r", encoding='utf-8') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

app: FastAPI = FastAPI()

#MACRO_SERVER_ID = "{MACRO_SERVER_ID}"
MACRO_SERVER_ID = config["destination-server-name"]
SERVER_IP = config["cloud-mqtt"]
CLIENT_ID = config["client-id"]

@app.get("/")
async def root():
    """Root endpoint for the server."""
    return {"message": "Hello World"}

# Create

@app.post("/building/create")
async def create_building(new_building: Building):
    """Create a building."""
    print(new_building)
    async with Client(SERVER_IP) as client:
        await client.subscribe(f"{CLIENT_ID}/callback")
        await client.publish(f"{MACRO_SERVER_ID}/building/new",
                             payload=json.dumps(
                                 {
                                    "name": new_building.name,
                                    "callback": f"{CLIENT_ID}/callback"
                                    }
                                    ))
        for message in client.messages:
            print(message.payload.decode())
            return {"callback": json.loads(message.payload.decode())}
    return {"message": "Building Created"}

@app.post("/space/create")
async def create_space(new_space: Space):
    """Create a space."""
    async with Client(SERVER_IP) as client:
        await client.subscribe(f"{CLIENT_ID}/callback")
        await client.publish(f"{MACRO_SERVER_ID}/space/new",
                             payload=json.dumps(
                                 {
                                    "name": new_space.name,
                                    "building": new_space.building,
                                    "callback": f"{CLIENT_ID}/callback"
                                    }
                                    ))
        for message in client.messages:
            print(message.payload.decode())
            return {"callback": json.loads(message.payload.decode())}
    return {"message": "Space Created"}

@app.post("/room/create")
async def create_room(new_room: Room):
    """Create a room."""
    async with Client(SERVER_IP) as client:
        await client.subscribe(f"{CLIENT_ID}/callback")
        await client.publish(f"{MACRO_SERVER_ID}/room/new",
                             payload=json.dumps(
                                 {
                                    "name": new_room.name,
                                    "space": new_room.space,
                                    "building": new_room.building,
                                    "callback": f"{CLIENT_ID}/callback"
                                    }
                                    ))
        for message in client.messages:
            print(message.payload.decode())
            return {"callback": json.loads(message.payload.decode())}
    return {"message": "Room Created"}

# List

@app.get("/location/list")
async def list_locations():
    """List all locations."""
    payload = ""
    async with Client(SERVER_IP) as client:
        await client.subscribe(f"{CLIENT_ID}/callback")
        await client.publish(f"{MACRO_SERVER_ID}/room/list",
                             payload=json.dumps(
                                 {
                                    "callback": f"{CLIENT_ID}/callback"
                                    }
                                ))
        async for message in client.messages:
            print(message.payload.decode())
            payload = message.payload.decode()
            return {"callback": json.loads(payload)}
    return {"message": ""}

@app.get("/building/list")
async def list_buildings():
    """List all buildings."""
    payload = ""
    async with Client(SERVER_IP) as client:
        await client.subscribe(f"{CLIENT_ID}/callback")
        await client.publish(f"{MACRO_SERVER_ID}/building/list",
                             payload=json.dumps(
                                 {
                                    "callback": f"{CLIENT_ID}/callback"
                                    }
                                ))
        async for message in client.messages:
            print(message.payload.decode())
            payload = message.payload.decode()
            return {"callback": json.loads(payload)}
    return {"message": ""}

@app.get("/space/list")
async def list_spaces():
    """List all spaces."""
    payload = ""
    async with Client(SERVER_IP) as client:
        await client.subscribe(f"{CLIENT_ID}/callback")
        await client.publish(f"{MACRO_SERVER_ID}/space/list",
                             payload=json.dumps(
                                 {
                                    "callback": f"{CLIENT_ID}/callback"
                                    }
                                ))
        async for message in client.messages:
            print(message.payload.decode())
            payload = message.payload.decode()
            return {"callback": json.loads(payload)}
    return {"message": ""}

@app.get("/room/list")
async def list_rooms():
    """List all rooms."""
    print("list_rooms")
    payload = ""
    async with Client(SERVER_IP) as client:
        await client.subscribe(f"{CLIENT_ID}/callback")
        print(f"subscribing to {CLIENT_ID}/callback")
        await client.publish(f"{MACRO_SERVER_ID}/room/list",
                             payload=json.dumps(
                                 {
                                    "callback": f"{CLIENT_ID}/callback"
                                    }
                                ))
        print("publishing to {MACRO_SERVER_ID}/room/list")
        async for message in client.messages:
            print(message.payload.decode())
            payload = message.payload.decode()
            return {"callback": json.loads(payload)}
    return {"message": ""}

# Devices

@app.get("/devices/list_all")
async def list_all_devices():
    """List all devices."""
    payload = ""
    print("list_all_devices")
    async with Client(SERVER_IP) as client:
        await client.subscribe(f"{CLIENT_ID}/callback")
        await client.publish(f"{MACRO_SERVER_ID}/devices/list_all",
                             payload=json.dumps(
                                 {
                                    "callback": f"{CLIENT_ID}/callback"
                                    }
                                ))
        async for message in client.messages:
            print(message.payload.decode())
            payload = message.payload.decode()
            return {"callback": json.loads(payload)}
    return {"message": ""}

@app.get("/devices/list")
async def list_devices():
    """List only registered devices."""
    payload = ""
    async with Client(SERVER_IP) as client:
        await client.subscribe(f"{CLIENT_ID}/callback")
        await client.publish(f"{MACRO_SERVER_ID}/devices/list",
                             payload=json.dumps(
                                 {
                                    "callback": f"{CLIENT_ID}/callback"
                                    }
                                ))
        async for message in client.messages:
            print(message.payload.decode())
            payload = message.payload.decode()
            return {"callback": json.loads(payload)}
    return {"message": ""}

@app.get("/devices/available")
async def list_available():
    """List only available devices."""
    payload = ""
    async with Client(SERVER_IP) as client:
        await client.subscribe(f"{CLIENT_ID}/callback")
        await client.publish(f"{MACRO_SERVER_ID}/devices/available",
                             payload=json.dumps(
                                 {
                                    "callback": f"{CLIENT_ID}/callback"
                                    }
                                ))
        async for message in client.messages:
            print(message.payload.decode())
            payload = message.payload.decode()
            return {"callback": json.loads(payload)}
    return {"message": ""}

@app.get("/devices/all_drivers")
async def list_all_drivers():
    """List all drivers."""
    payload = ""
    async with Client(SERVER_IP) as client:
        await client.subscribe(f"{CLIENT_ID}/callback")
        await client.publish(f"{MACRO_SERVER_ID}/devices/all_drivers",
                             payload=json.dumps(
                                 {
                                    "callback": f"{CLIENT_ID}/callback"
                                    }
                                ))
        async for message in client.messages:
            print(message.payload.decode())
            payload = message.payload.decode()
            return {"callback": json.loads(payload)}
    return {"message": ""}

@app.post("/devices/register")
async def register_device(device: Device):
    """Register a device."""
    async with Client(SERVER_IP) as client:
        await client.subscribe(f"{CLIENT_ID}/callback")
        await client.publish(f"{MACRO_SERVER_ID}/devices/register",
                             payload=json.dumps(
                                 {
                                    "id": device.id,
                                    "name": device.name,
                                    "driver": device.driver,
                                    "room_id": device.room_id,
                                    "callback": f"{CLIENT_ID}/callback"
                                    }
                                ))
        for message in client.messages:
            print(message.payload.decode())
            return {"callback": json.loads(message.payload.decode())}
    return {"message": "Device Registered"}

@app.post("/devices/{driver}/new_device")
async def new_device(driver: str, device: DeviceByDriver):
    """Create a new device."""
    async with Client(SERVER_IP) as client:
        await client.subscribe(f"{CLIENT_ID}/callback")
        await client.publish(f"{MACRO_SERVER_ID}/devices/{driver}/new_device",
                             payload=json.dumps(
                                 {
                                    "device_type": device.device_type,
                                    "room_id": device.room_id,
                                    "device_name": device.device_name,
                                    "data": device.data,
                                    "callback": f"{CLIENT_ID}/callback"
                                    }
                                ))
        for message in client.messages:
            print(message.payload.decode())
            return {"callback": json.loads(message.payload.decode())}
    return {"message": "Device Created"}

@app.post("/devices/{device}")
async def device_command(device: str, command: Command):
    """Send a command to a device."""
    async with Client(SERVER_IP) as client:
        await client.subscribe(f"{CLIENT_ID}/callback")
        await client.publish(f"{MACRO_SERVER_ID}/devices/{device}",
                             payload=json.dumps(
                                 {
                                    "cmnd": command.cmnd,
                                    "set_temperature": command.set_temperature,
                                    "set_mode": command.set_mode,
                                    "set_fan_speed": command.set_fan_speed,
                                    "callback": f"{CLIENT_ID}/callback"
                                    }
                                ))
        #for message in client.messages:
        #    print(message.payload.decode())
        #    return {"callback": json.loads(message.payload.decode())}
    return {"message": "Command Sent"}


def main():
    """Run the server."""
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        reload=False
    )


if __name__ == "__main__":
    main()
