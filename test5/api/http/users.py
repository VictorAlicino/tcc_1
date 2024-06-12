"""HTTP API Users Endpoints"""
from fastapi import APIRouter, status, Response
from fastapi.responses import HTMLResponse
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request
from db.models import OpusUser
import db.users as opus_users
import db.localservers as opus_servers
from db.database import DB
from configurations.config import OpenConfig
from api.http.models import Role

config = OpenConfig()
db = DB(config["database"]["url"])

router = APIRouter(
    prefix="/users",
    tags=["Users"],
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

@router.get("/users")
async def get_all_users():
    """Users endpoint for the server."""
    return opus_users.get_all_users(next(db.get_db()))

@router.delete("/users/delete/{user_id}")
async def delete_user(user_id: str):
    """Delete user endpoint for the server."""
    db_session = next(db.get_db())
    user = opus_users.get_user_by_id(db_session, user_id)
    if user:
        return opus_users.delete_user(db_session, user)
    return "User not found", status.HTTP_404_NOT_FOUND

@router.post("/users/set_role")
async def set_user_role(role: Role):
    """Set user role endpoint for the server."""
    db_session = next(db.get_db())
    return opus_servers.set_user_server_role(
        db_session,
        role.user_id,
        role.server_id,
        role.role
    )

@router.get("/users/server/{user_id}")
async def get_user_servers(user_id: str):
    """Get user servers endpoint for the server."""
    db_session = next(db.get_db())
    return opus_users.get_servers_of_user(db_session, user_id)
