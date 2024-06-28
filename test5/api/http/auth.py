"""HTTP API Authentications Endpoints"""
import logging
from fastapi import APIRouter, status, Response
from fastapi.responses import RedirectResponse
from starlette.requests import Request
from authlib.integrations.starlette_client import OAuth
from jose import JWTError, jwt

from configurations.config import CONFIG
from db.database import DB
import db.users as opus_users
from db.models import OpusUser

from api.http.models import ConductorLogin, User

log = logging.getLogger(__name__)
db = DB(CONFIG["database"]["url"])

router = APIRouter(
    prefix="/auth",
    tags=["Authentications"],
)

# Google OAuth2
oauth = OAuth()
oauth.register(
    name = 'google',
    server_metadata_url = 'https://accounts.google.com/.well-known/openid-configuration',
    client_id = CONFIG['google-api']['client_id'],
    client_secret = CONFIG['google-api']['client_secret'],
    client_kwargs = {
        'scope': 'openid email profile',
        'redirect_uri': 'http://localhost:8000/auth'
    }
)

@router.post("/conductor_request")
async def conductor_login(request: ConductorLogin):
    """Conductor login endpoint for the server."""
    print(request)
    db_session = next(db.get_db())
    user = opus_users.get_user_by_google_sub(db_session, request.google_sub)
    log.debug(f'{user.name} has logged in via Conductor')
    if user:
        return RedirectResponse(url="/login")
    return RedirectResponse(url="new_user")

@router.get("/login")
async def login(user: User):
    """Login endpoint for the server."""
    # Print the request
    print(user)
    return Response(
        content="You have logged in",
        status_code=status.HTTP_200_OK
    )

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

