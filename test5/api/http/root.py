"""HTTP API endpoints for the server."""
from fastapi import FastAPI, status, Response
from fastapi.responses import HTMLResponse
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request
from db.models import OpusUser
import db.users as opus_users
import db.localservers as opus_servers
from db.database import DB
from configurations.config import OpenConfig

from api.http.users import router as user_router
from api.http.localservers import router as server_router

from api.index import index_home_page
config = OpenConfig()

# Tag Metadata
tags_metadata = [
    {
        "name": "Users",
        "description": "Operations with users. The `/users` endpoint returns a list of all users.",
    },
    {
        "name": "Opus Server",
        "description": "Operations with Opus Server. "
            "The `/servers` endpoint returns a list of all servers.",
    },
    {
        "name": "Root",
        "description": "Root endpoint for the server."
    }
]

# FASTAPI instance
api: FastAPI = FastAPI(
    title="Opus Server API",
    description="This is the Opus Server API.",
    version="0.0.1",
    terms_of_service="Nah, no terms of service. It's just an example.",
    contact={
        "name": "Victor Alicino",
        "url": "https://github.com/victoralicino",
        "email": "victor.alicino@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)
api.add_middleware(SessionMiddleware, secret_key="your-secret")

api.include_router(user_router)
api.include_router(server_router)