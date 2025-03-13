"""HTTP API Authentications Endpoints"""
import datetime
import logging
import json
import httpx
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

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"


# Conductor Auth -----------------------------------------------------------------

@router.post("/register")
async def conductor_register(request: Request, db_session=Depends(db.get_db)):
    """Conductor register endpoint for the server"""
    # Check if the user is authenticated
    token = await request.json()
    token = token['payload']
    if maestro_users.get_user_by_google_sub(db_session, token['id']):
        return JSONResponse(
            content={
                "message": f"Mr(s). {token['givenName']} {token['familyName']} is already registered",
                "email": token['email']
            },
            status_code=200
        )
    user = MaestroUser(
        google_sub = token['id'],
        email = token['email'],
        name = token['name'],
        given_name = token['givenName'],
        family_name = token['familyName'],
        picture_url = token['photo']
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
    user = maestro_users.get_user_by_google_sub(db_session, request.google_sub)
    if user is None:
        log.warning(f"{request.email} tried to login but is not authorized")
        return JSONResponse(
            content="User not found",
            status_code=404
        )
        
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
