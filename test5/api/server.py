"""API endpoints for the server."""
import yaml
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
#from aiomqtt import Client
#from api.models import Building, Space, Room, Device, DeviceByDriver, Command

# Load YAML file
with open("config.yaml", "r", encoding='utf-8') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

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
    except Exception as e:
        print(e)
        return str(e)
    #print(token)
    print(f"New User Logged In:\n"
          f"Name: {token['userinfo']['name']}\nEmail: {token['userinfo']['email']}")
