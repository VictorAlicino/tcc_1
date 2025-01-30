"""Main entry point for the application."""
import logging.config
import sys
import os
import threading
import json
import asyncio
from decouple import config as env
import uvicorn
import logging
from db.database import DB
from configurations.config import OpenConfig
from logs.logger import define_log
from api.mqtt.basic_comms import server_login_listener
from api.rest._root import api

# MQTT Async Guard
if sys.platform.lower() == "win32" or os.name.lower() == "nt":
    from asyncio import set_event_loop_policy, WindowsSelectorEventLoopPolicy
    set_event_loop_policy(WindowsSelectorEventLoopPolicy())

def _main() -> None:
    """Main entry point for the application."""
    # Logging
    log = define_log(log_level="DEBUG")

    # Start the database
    db = DB()
    db.create_all()

    # Start the MQTT API
    _new_server_listener_thread = threading.Thread(
        target=asyncio.run,
        args=(server_login_listener(),)
        )
    _new_server_listener_thread.start()

    # Start the REST API
    uvicorn.run(
        "api.rest._root:api",
        host="0.0.0.0",
        port=9530,
        log_config=log,
        reload=True
    )

if __name__ == "__main__":
    _main()
