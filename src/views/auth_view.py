import logging
from datetime import timedelta

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from controllers.auth_controller import AuthController, ACCESS_TOKEN_EXPIRE_MINUTES
from custom_types.user_types import UserCreate
from custom_types.token_types import Token

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", status_code=status.HTTP_201_CREATED, summary="Register new user")
def register_user(user: UserCreate):

    user_id = AuthController.create_user(username=user.username, password=user.password)

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error: User does not existe or fail in creation"
        )
    
    return {"message": "User created with success!", "user_id": user_id}

@router.post("/token", response_model=Token, summary="Login (Get Token)")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = AuthController.authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User or password is incorrect",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = AuthController.create_acces_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

