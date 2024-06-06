"""HTTP API endpoints for the server."""
import json
import yaml
from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
from db.models import OpusUser
import db.users as opus_users
import db.localservers as opus_servers
from db.database import DB
from api.http_models import Role

# Load YAML file
with open("config.yaml", "r", encoding='utf-8') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

db = DB(config["database"]["url"])
api: FastAPI = FastAPI()
api.add_middleware(SessionMiddleware, secret_key="your-secret")
oauth = OAuth()

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

@api.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint for the server."""
    return """
    <html>
        <head>
            <title>Server Works!</title>
        </head>
        <body>
            <h1>Hello World!</h1>
        </body>
    </html>
    """

@api.get("/login")
async def login(request: Request):
    """Login endpoint for the server."""
    # Print the request
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@api.get("/logout")
async def logout(request: Request):
    """Logout endpoint for the server."""
    return request

@api.get("/auth")
async def auth(request: Request):
    """Auth endpoint for the server."""
    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception as e: # pylint: disable=broad-except
        print(e)
        # Return 401
        return "Unauthorized", status.HTTP_401_UNAUTHORIZED

    # Check if the user is authenticated
    if opus_users.get_user_by_google_sub(next(db.get_db()), token['userinfo']['sub']):
        return "User already exists"
    user = OpusUser(
        google_sub = token['userinfo']['sub'],
        email = token['userinfo']['email'],
        name = token['userinfo']['name'],
        given_name = token['userinfo']['given_name'],
        family_name = token['userinfo']['family_name'],
        picture = token['userinfo']['picture']
    )
    opus_users.create_user(next(db.get_db()), user)
    return (f"Mr(s). {user.given_name} {user.family_name} "
            f"has been created with the email {user.email}")

@api.get("/users")
async def get_all_users():
    """Users endpoint for the server."""
    return opus_users.get_all_users(next(db.get_db()))

@api.delete("/users/delete/{user_id}")
async def delete_user(user_id: str):
    """Delete user endpoint for the server."""
    db_session = next(db.get_db())
    user = opus_users.get_user_by_id(db_session, user_id)
    if user:
        return opus_users.delete_user(db_session, user)
    return "User not found", status.HTTP_404_NOT_FOUND

@api.get("/servers")
async def get_all_servers():
    """Servers endpoint for the server."""
    return opus_servers.get_all_servers(next(db.get_db()))

@api.delete("/servers/delete/{server_id}")
async def delete_server(server_id: str):
    """Delete server endpoint for the server."""
    db_session = next(db.get_db())
    server = opus_servers.get_server_by_id(db_session, server_id)
    if server:
        return opus_servers.delete_server(db_session, server)
    return "Server not found", status.HTTP_404_NOT_FOUND

@api.post("/users/set_role")
async def set_user_role(role: Role):
    """Set user role endpoint for the server."""
    db_session = next(db.get_db())
    return opus_servers.set_user_server_role(
        db_session,
        role.user_id,
        role.server_id,
        role.role
    )

@api.get("/servers/admins/{server_id}")
async def get_server_admins(server_id: str):
    """Get server admins endpoint for the server."""
    db_session = next(db.get_db())
    result =  opus_servers.get_server_admins(db_session, server_id)
    if result:
        admins = []
        for row in result:
            user = opus_users.get_user_by_id(db_session, row.user_id)
            admins.append((user.user_id, user.email))
        return {
            "server_id": server_id,
            "admins": admins
        }
    return "Server not found", status.HTTP_404_NOT_FOUND
