"""Main entry point for the application."""
import sys
import os
import logging
import uvicorn
import yaml
from initializers import define_log

log = logging.getLogger(__name__)

if sys.platform.lower() == "win32" or os.name.lower() == "nt":
    from asyncio import set_event_loop_policy, WindowsSelectorEventLoopPolicy
    set_event_loop_policy(WindowsSelectorEventLoopPolicy())

# Directories Path
DIRS: dict = {
    "LOGS": "logs",
    "ROUTES": "routes",
}

# Load YAML file
with open("config.yaml", "r", encoding='utf-8') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

def _main() -> None:
    define_log(DIRS, "DEBUG")

    # Run the server
    log.info("Starting server")
    uvicorn.run(
        "api.server:api",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        reload=False
    )

if __name__ == "__main__":
    _main()
