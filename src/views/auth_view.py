import logging
import jwt

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from controllers.auth_controller import AuthController, SECRET_KEY, ALGORITHM
from custom_types.user_types import UserCreate
from custom_types.token_types import Token, TokenRefreshRequest

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        jti = payload.get("jti")

        if AuthController.is_jti_blacklisted(jti):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been revoked",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return payload
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
def admin_access_required(payload: dict = Depends(get_current_user)):
    role = payload.get("role")
    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator access required"
        )
    return payload

@router.post("/register", status_code=status.HTTP_201_CREATED, summary="Register a new user")
def register_user(user: UserCreate):
    user_id = AuthController.create_user(username=user.username, email=user.email, password=user.password, role="user")
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists or failed to create user",
        )
    
    return dict(message="User created successfully", user_id=user_id)

@router.post("/token", response_model=Token, summary="Login and get Access/Refresh tokens")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = AuthController.authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    tokens = AuthController.create_tokens(username=user.username, user_id=user.id, role=user.role)
    
    return {
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
        "token_type": "bearer"
    }

@router.post("/refresh", summary="Refresh Access Token")
def refresh_token(request: TokenRefreshRequest):
    new_token = AuthController.refresh_access_token(request.refresh_token)
    
    if not new_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token invalid or revoked",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    return {
        "access_token": new_token["access_token"],
        "refresh_token": request.refresh_token,
        "token_type": "bearer"
    }


@router.post("/forgot-password", summary="Request password reset")
def forgot_password(request: PasswordResetRequest):
    token = AuthController.generate_reset_token(request.email)
    if token:
        AuthController.send_email_mock(request.email, "Reset Password", f"Token: {token}")
    return {"message": "If email exists, instructions were sent"}

@router.post("/reset-password", summary="Confirm new password")
def reset_password(data: PasswordResetConfirm):
    if not AuthController.reset_password(data.token, data.new_password):
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    return {"message": "Password reset successfully"}


@router.get("/me", response_model=UserResponse, summary="Get profile")
def get_profile(current_user: dict = Depends(get_current_user)):
    user = AuthController.get_user_by_name(current_user['sub'])
    return user

@router.patch("/me", summary="Update profile")
def update_profile(data: UserUpdate, current_user: dict = Depends(get_current_user)):
    if not AuthController.update_user(current_user['id'], data.email, data.password):
        raise HTTPException(status_code=400, detail="Update failed")
    return {"message": "Updated successfully"}

@router.delete("/me", summary="Delete account")
def delete_account(current_user: dict = Depends(get_current_user)):
    if not AuthController.delete_user(current_user['id']):
        raise HTTPException(status_code=500, detail="Delete failed")
    return {"message": "Account deleted"}

@router.post("/invite", summary="Invite user (REQ 11)")
def invite_user(invite: InviteRequest, current_user: dict = Depends(get_current_user)):
    AuthController.send_email_mock(invite.email, "Invitation", f"{current_user['sub']} invited you to play!")
    return {"message": f"Invitation sent to {invite.email}"}

@router.post("/logout", status_code=status.HTTP_200_OK, summary="Logout (Revoke Token)")
def logout_user(token: str = Depends(oauth2_scheme)):
    success = AuthController.revoke_token(token)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to logout due to server error"
        )

    return {"message": "Successfully logged out"}