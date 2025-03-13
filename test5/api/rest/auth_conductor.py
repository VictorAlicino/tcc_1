"""HTTP API Authentications Endpoints"""
import datetime
import logging
import json
from fastapi import APIRouter, HTTPException, status, Response, Depends
from fastapi.security import OAuth2AuthorizationCodeBearer, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.requests import Request
from authlib.integrations.starlette_client import OAuth
from jose import JWTError, jwt

from configurations.config import CONFIG
from db.database import DB
import db.users as maestro_users
from db.models import MaestroUser

from api.rest._api_models import ConductorLogin, ConductorRegister, User, VerifyToken

log = logging.getLogger(__name__)
db = DB()

router = APIRouter(
    prefix="/auth/conductor",
    tags=["Authentications [Conductor]"],
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
        'redirect_uri': 'http://localhost:9530/register'
    }
)

# Internal OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Conductor Auth -----------------------------------------------------------------

@router.post("/register")
async def conductor_register(request: Request, db_session=Depends(db.get_db)):
    """Conductor register endpoint for the server"""
    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception as e: # pylint: disable=broad-except
        print(e)
        # Return 401
        return "Unauthorized", status.HTTP_401_UNAUTHORIZED

    # Check if the user is authenticated
    print(token)
    if maestro_users.get_user_by_google_sub(db_session, token['userinfo']['sub']):
        return "User already exists"
    user = MaestroUser(
        google_sub = token['userinfo']['sub'],
        email = token['userinfo']['email'],
        name = token['userinfo']['name'],
        given_name = token['userinfo']['given_name'],
        family_name = token['userinfo']['family_name'],
        picture = token['userinfo']['picture']
    )
    maestro_users.create_user(db_session, user)
    return JSONResponse(
        content={
            "message": f"Mr(s). {user.given_name} {user.family_name} has been created",
            "email": user.email
        },
        status_code=201
    )

@router.post("/login")
async def conductor_login(request: ConductorLogin, db_session=Depends(db.get_db)):
    """Conductor login endpoint for the server."""
    print(request)
    user = maestro_users.get_user_by_google_sub(db_session, request.google_sub)
    if user is None:
        log.warning(f"{request.email} tried to login but is not authorized")
        log.info(f"Registering {request.email} as a new user")
        # setting up a new request
        new_request = Request(
            {
                'google_sub': request.google_sub,
                'email': request.email
            }
        )
        token = await oauth.google.authorize_access_token(new_request)
        user = MaestroUser(
            google_sub = token['userinfo']['sub'],
            email = token['userinfo']['email'],
            name = token['userinfo']['name'],
            given_name = token['userinfo']['given_name'],
            family_name = token['userinfo']['family_name'],
            picture = token['userinfo']['picture']
        )
        maestro_users.create_user(db_session, user)
        user = maestro_users.get_user_by_google_sub(db_session, request.google_sub)
        
    log.debug(f'{user.name} has logged in via Conductor')    
    exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)

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

@router.get("/logout")
async def logout(request: Request):
    """Logout endpoint for the server."""
    return request

@router.get("/refresh_token")
async def refresh_token(request: Request):
    """Refresh token endpoint for the server."""
    return request

@router.get("/verify_token")
async def verify_token(request: Request):
    """Verify token endpoint for the server."""
    return request
