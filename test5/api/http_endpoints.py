"""HTTP API endpoints for the server."""
import yaml
from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
from db.models import OpusUser
from db.users import get_user_by_google_sub, create_user
from db.database import DB
#from aiomqtt import Client
#from api.models import Building, Space, Room, Device, DeviceByDriver, Command

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
    if get_user_by_google_sub(next(db.get_db()), token['userinfo']['sub']):
        return "User already exists"
    user = OpusUser(
        google_sub = token['userinfo']['sub'],
        email = token['userinfo']['email'],
        name = token['userinfo']['name'],
        given_name = token['userinfo']['given_name'],
        family_name = token['userinfo']['family_name'],
        picture = token['userinfo']['picture']
    )
    create_user(next(db.get_db()), user)
    return (f"Mr(s). {user.given_name} {user.family_name} "
            f"has been created with the email {user.email}")
