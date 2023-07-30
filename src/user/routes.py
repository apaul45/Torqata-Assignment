# This is a basic authentication system that only supports login at the moment
import sys

sys.path.insert(0, "..")

from dotenv import load_dotenv
import os

from fastapi import Depends, APIRouter, HTTPException
from user.models import Token
from user.service import SQLUserService as UserService
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt

load_dotenv()

router = APIRouter(tags=["users"])

# Using OAuth2 with Password flow and Bearer token (ie, header Authorization with "Bearer {token}")
# As the tokenUrl is token, the user will be sending their info to the path "/token" to receive their token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# pwd_context for checking and hashing passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Algorithm and secret key for encoding/decoding JWTs
algorithm = "HS256"
secret_key = os.getenv("JWT_SECRET")


# OAuth2PasswordRequestForm is a dependency that creates a form with the entered username and password
# Since this routes path is "/token", it will be called once the user enters their info into the request form
@router.post("/token", response_model=Token)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: UserService = Depends(UserService),
):
    user = await service.get_user(form_data.username)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username")

    pass_verification = pwd_context.verify(form_data.password, user["passwordHash"])

    if not pass_verification:
        raise HTTPException(status_code=400, detail="Incorrect password")

    # Create and send a JWT for the user to use for authorization
    token = jwt.encode({"user": user["username"]}, secret_key, algorithm=algorithm)
    return {"access_token": token}


# From FastAPI documentation: this will serve as authorization for all routes
# Once the user authenticates, oauth2_scheme will check for their token, which is why its a dependency
async def get_current_user(
    token: str = Depends(oauth2_scheme), service: UserService = Depends(UserService)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    username = None

    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        username = payload.get("user")

        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = await service.get_user(username)

    if user is None:
        raise credentials_exception

    return user
