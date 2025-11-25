import os
import jwt
from datetime import datetime, timedelta
from typing import Optional

from model.manager import DBManager
from model.models import User

SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "heyho_0102")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class AuthController:

    @staticmethod
    def get_user_by_name(username: str) -> Optional[User]:
        try:
            session = DBManager.get_session()
            user = session.query(User).filter(User.username == username).first()
            return user
        except Exception as e:
            print(f"Erro ao buscar usuário: {e}")
            return None
        finally:
            session.close()
    
    @staticmethod
    def create_user(username: str, password: str) -> Optional[User]:
        if AuthController.get_user_by_name(username):
            return None
        
        hashed_pass = User.hash_password(password)

        new_user = User(username=username, hashed_password = hashed_pass)

        try:
            session = DBManager.get_session()
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            return new_user.id
        except Exception as e:
            session.rollback()
            print(f"Error when creating user: {e}")
            return None
        finally:
            session.close()

    @staticmethod
    def authenticate_user(username: str, password: str) -> Optional[User]:

        user = AuthController.get_user_by_name(username)
        if not user:
            return None
        
        if not user.verify_password(password):
            return None
        
        return user
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:

        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})

        encoded_jwt = jwt.enconde(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    

