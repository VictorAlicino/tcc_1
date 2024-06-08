"""Main entry point for the application."""
import sys
import os
import threading
import asyncio
import uvicorn
import yaml
from db.database import DB
from api.mqtt_endpoints import server_login_listener

if sys.platform.lower() == "win32" or os.name.lower() == "nt":
    from asyncio import set_event_loop_policy, WindowsSelectorEventLoopPolicy
    set_event_loop_policy(WindowsSelectorEventLoopPolicy())

# Load YAML file
with open("config.yaml", "r", encoding='utf-8') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

def _main() -> None:
    # Start the database
    db = DB(config["database"]["url"])
    db.create_all()

    # Start the MQTT client
    _new_server_listener_thread = threading.Thread(
        target=asyncio.run,
        args=(server_login_listener(),)
        )
    _new_server_listener_thread.start()

    # Run the server
    uvicorn.run(
        "api.http_endpoints:api",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        reload=True
    )

if __name__ == "__main__":
    _main()
