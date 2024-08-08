"""HTTP API Authentications Endpoints"""
import datetime
import logging
from fastapi import APIRouter, HTTPException, status, Response
from fastapi.responses import RedirectResponse
from starlette.requests import Request
from authlib.integrations.starlette_client import OAuth
from jose import JWTError, jwt

from configurations.config import CONFIG
from db.database import DB
import db.users as opus_users
from db.models import MaestroUser

from api.rest.models import ConductorLogin, ConductorRegister, User

log = logging.getLogger(__name__)
db = DB()

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

# Conductor Auth -----------------------------

@router.post("/conductor/register")
async def conductor_register(request: ConductorRegister):
    """Conductor register endpoint for the server"""
    print(request)
    return status.HTTP_200_OK

@router.post("/conductor/login")
async def conductor_login(request: ConductorLogin):
    """Conductor login endpoint for the server."""
    db_session = next(db.get_db())
    user = opus_users.get_user_by_google_sub(db_session, request.google_sub)
    if user is None:
        log.warning(f"{request.email} tried to login but is not authorized")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    log.debug(f'{user.name} has logged in via Conductor')    
    exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)

    # Create a JWT token
    payload = {
        'sub': user.google_sub,
        'exp': exp
    }

    access_token = jwt.encode(payload, CONFIG['api-secrets']['secret_key'], algorithm='HS256')

    return {
        'access_token': access_token,
        'exp': exp,
        'token_type': 'bearer'
    }

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
    user = MaestroUser(
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

