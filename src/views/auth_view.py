import logging
import jwt
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from controllers.auth_controller import AuthController, SECRET_KEY, ALGORITHM
from custom_types.user_types import (
    UserCreate, UserResponse, UserUpdate, 
    PasswordResetRequest, PasswordResetConfirm, InviteRequest
)
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
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token revoked", headers={"WWW-Authenticate": "Bearer"}
            )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token", headers={"WWW-Authenticate": "Bearer"})

def admin_access_required(payload: dict = Depends(get_current_user)):
    if payload.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Administrator access required")
    return payload

@router.post("/register", status_code=status.HTTP_201_CREATED, summary="Register user")
def register_user(user: UserCreate):
    user_id = AuthController.create_user(username=user.username, email=user.email, password=user.password, role="user")
    if not user_id:
        raise HTTPException(status_code=400, detail="Username or Email already exists")
    return dict(message="User created successfully", user_id=user_id)

@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = AuthController.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect credentials")
    tokens = AuthController.create_tokens(username=user.username, user_id=user.id, role=user.role)
    return tokens

@router.post("/refresh")
def refresh(request: TokenRefreshRequest):
    new_token = AuthController.refresh_access_token(request.refresh_token)
    if not new_token: raise HTTPException(status_code=401, detail="Invalid refresh token")
    return new_token

@router.post("/forgot-password", summary="Request password reset")
def forgot_password(request: PasswordResetRequest):
    # CORREÇÃO: Nome do método atualizado para bater com o controller
    AuthController.password_reset_email(request.email)
    return {"message": "Se o e-mail estiver cadastrado, as instruções foram enviadas."}

@router.post("/invite", summary="Invite user")
def invite_user(invite: InviteRequest, current_user: dict = Depends(get_current_user)):
    inviter_name = current_user['sub'] 
    # CORREÇÃO: Nome do método atualizado
    sent = AuthController.invite_email(invite.email, inviter_name)
    if not sent:
         raise HTTPException(status_code=500, detail="Erro ao enviar convite. Tente novamente.")
    return {"message": f"Convite enviado para {invite.email}"}

@router.post("/reset-password", summary="Confirm new password")
def reset_password(data: PasswordResetConfirm):
    if not AuthController.reset_password(data.token, data.new_password):
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    return {"message": "Password reset successfully"}

@router.get("/me", response_model=UserResponse, summary="Get profile")
def get_profile(current_user: dict = Depends(get_current_user)):
    return AuthController.get_user_by_name(current_user['sub'])

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

@router.post("/logout", status_code=200)
def logout(token: str = Depends(oauth2_scheme)):
    AuthController.revoke_token(token)
    return {"message": "Logged out"}

# NOVO: Rota para listar usuários (Útil para Admin)
@router.get("/users", response_model=list[UserResponse], summary="List all users (Admin only)")
def list_users(current_user: dict = Depends(admin_access_required)):
    return AuthController.get_all_users()