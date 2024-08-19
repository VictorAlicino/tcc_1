"""HTTP API endpoints for the server."""
from fastapi import FastAPI, status, Response
from fastapi.responses import HTMLResponse
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request
from db.models import MaestroUser
import db.users as maestro_users
import db.localservers as opus_servers
from api.http_models import Role
from db.database import DB
from configurations.config import OpenConfig
from api.http_models import ServerUserList
from api.mqtt_server_comms import send_cmd_to_server

from api.index import index_home_page

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
oauth = OAuth()
config = OpenConfig()
db = DB()
oauth.register(
    name = 'google',
    server_metadata_url = 'https://accounts.google.com/.well-known/openid-configuration',
    client_id = config['google-api']['client_id'],
    client_secret = config['google-api']['client_secret'],
    client_kwargs = {
        'scope': 'openid email profile',
        'redirect_uri': 'http://localhost:8000/auth'
    }
)

@api.get("/", response_class=HTMLResponse, tags=["Root"])
async def root():
    """Root endpoint for the server."""
    return HTMLResponse(content=index_home_page, status_code=200)

# -------------------------------------------------------------------

@api.get("/servers", tags=["Opus Server"])
async def get_all_servers():
    """Servers endpoint for the server."""
    return opus_servers.get_all_servers(next(db.get_db()))

@api.delete("/servers/delete/{server_id}", tags=["Opus Server"])
async def delete_server(server_id: str):
    """Delete server endpoint for the server."""
    db_session = next(db.get_db())
    server = opus_servers.get_server_by_id(db_session, server_id)
    if server:
        return opus_servers.delete_server(db_session, server)
    return "Server not found", status.HTTP_404_NOT_FOUND

@api.get("/servers/admins/{server_id}", tags=["Opus Server"])
async def get_server_admins(server_id: str):
    """Get server admins endpoint for the server."""
    db_session = next(db.get_db())
    result =  opus_servers.get_server_admins(db_session, server_id)
    if result:
        admins = []
        for row in result:
            user = maestro_users.get_user_by_id(db_session, row.user_id)
            admins.append((user.user_id, user.email))
        return {
            "server_id": server_id,
            "admins": admins
        }
    return "Server not found", status.HTTP_404_NOT_FOUND

@api.post("/servers/assign_users", tags=["Opus Server"])
async def assign_users_to_server(server_user_list: ServerUserList):
    """Assign users to server endpoint for the server."""
    db_session = next(db.get_db())
    return opus_servers.assign_users_to_server(
        db_session,
        server_user_list.server_id,
        server_user_list.users
    )

@api.get("/servers/users/{server_id}", tags=["Opus Server"])
async def get_server_users(server_id: str):
    """Get server users endpoint for the server."""
    db_session = next(db.get_db())
    result =  opus_servers.get_server_users(db_session, server_id)
    if result:
        users = []
        for row in result:
            user = maestro_users.get_user_by_id(db_session, row.user_id)
            users.append((user.user_id, user.email))
        return {
            "server_id": server_id,
            "users": users
        }
    return "Server not found", status.HTTP_404_NOT_FOUND

@api.post("/cmd/{server_id}", tags=["Opus Server"])
async def command(server_id: str, cmd: dict):
    """Command endpoint for the server."""
    send_cmd_to_server(server_id, cmd)
    return "Command sent", status.HTTP_200_OK

# -------------------------------------------------------------------

@api.get("/login", tags=["Users"])
async def login(request: Request):
    """Login endpoint for the server."""
    # Print the request
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@api.get("/logout", tags=["Users"])
async def logout(request: Request):
    """Logout endpoint for the server."""
    return request

@api.get("/auth", tags=["Users"])
async def auth(request: Request):
    """Auth endpoint for the server."""
    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception as e: # pylint: disable=broad-except
        print(e)
        # Return 401
        return "Unauthorized", status.HTTP_401_UNAUTHORIZED

    # Check if the user is authenticated
    print(token)
    if maestro_users.get_user_by_google_sub(next(db.get_db()), token['userinfo']['sub']):
        return "User already exists"
    user = MaestroUser(
        google_sub = token['userinfo']['sub'],
        email = token['userinfo']['email'],
        name = token['userinfo']['name'],
        given_name = token['userinfo']['given_name'],
        family_name = token['userinfo']['family_name'],
        picture = token['userinfo']['picture']
    )
    maestro_users.create_user(next(db.get_db()), user)
    return (f"Mr(s). {user.given_name} {user.family_name} "
            f"has been created with the email {user.email}")

@api.get("/users", tags=["Users"])
async def get_all_users():
    """Users endpoint for the server."""
    return maestro_users.get_all_users(next(db.get_db()))

@api.delete("/users/delete/{user_id}", tags=["Users"])
async def delete_user(user_id: str):
    """Delete user endpoint for the server."""
    db_session = next(db.get_db())
    user = maestro_users.get_user_by_id(db_session, user_id)
    if user:
        return maestro_users.delete_user(db_session, user)
    return "User not found", status.HTTP_404_NOT_FOUND

@api.post("/users/set_role", tags=["Users"])
async def set_user_role(role: Role):
    """Set user role endpoint for the server."""
    db_session = next(db.get_db())
    return opus_servers.set_user_server_role(
        db_session,
        role.user_id,
        role.server_id,
        role.role
    )

@api.get("/users/server/{user_id}", tags=["Users"])
async def get_user_servers(user_id: str):
    """Get user servers endpoint for the server."""
    db_session = next(db.get_db())
    return maestro_users.get_servers_of_user(db_session, user_id)
