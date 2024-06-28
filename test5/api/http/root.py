"""HTTP API endpoints for the server."""
from fastapi import FastAPI, status, Response
from fastapi.responses import HTMLResponse
from starlette.middleware.sessions import SessionMiddleware
from configurations.config import CONFIG
import logging

from api.http.users import router as user_router
from api.http.localservers import router as server_router
from api.http.auth import router as auth_router

from api.http.index import index_home_page

# Logger
log = logging.getLogger(__name__)

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
    title="Maestro",
    description="This is the Opus Maestro API.",
    version="0.0.2",
    terms_of_service="Nah, no terms of service. It's just an example.",
    contact={
        "name": "Victor Alicino",
        "url": "https://github.com/victoralicino",
        "email": "victor.alicino@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }
)

api.add_middleware(SessionMiddleware, secret_key="your-secret")
api.include_router(auth_router)
api.include_router(server_router)
api.include_router(user_router)

@api.get("/", response_class=HTMLResponse, tags=["Root"])
async def root():
    """Root endpoint for the server."""
    return HTMLResponse(content=index_home_page, status_code=200)