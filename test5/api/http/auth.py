"""HTTP API Authentications Endpoints"""
from fastapi import APIRouter, status, Response
from starlette.requests import Request
from authlib.integrations.starlette_client import OAuth
from jose import JWTError, jwt

from configurations.config import OpenConfig
from db.database import DB
import db.users as opus_users
from db.models import OpusUser

from api.http.models import ConductorLogin

config = OpenConfig()
db = DB(config["database"]["url"])

router = APIRouter(
    prefix="/auth",
    tags=["Authentications"],
)

# Google OAuth2
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

@router.post("/request")
async def conductor_login(request: ConductorLogin):
    """Conductor login endpoint for the server."""
    print(request)
    db_session = next(db.get_db())
    user = opus_users.get_user_by_google_sub(db_session, request.google_sub)
    print(f'{user.name} has logged in via Conductor')
    if user:
        return user
    return "User not found", status.HTTP_404_NOT_FOUND

@router.get("/login")
async def login(request: Request):
    """Login endpoint for the server."""
    # Print the request
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/logout")
async def logout(request: Request):
    """Logout endpoint for the server."""
    return request

@router.get("/auth")
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

