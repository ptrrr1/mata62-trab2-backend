import os
import jwt
import uuid
from datetime import datetime, timedelta
from typing import Optional

from model import dbmanager
from model.models import User, TokenBlockList

import smtplib
from email.message import EmailMessage

SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "heyho_0102")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 1

class AuthController:

    @staticmethod
    def get_user_by_name(username: str) -> Optional[User]:
        session = None
        try:
            session = dbmanager.session
            user = session.query(User).filter(User.username == username).first()
            return user
        except Exception as e:
            print(f"Error fetching user: {e}")
            return None
        finally:
            if session:
                session.close()

    @staticmethod
    def create_user(username: str, email:str, password: str, role: str = "user") -> Optional[int]:
        session = None
        try:
            session = dbmanager.session
            existing = session.query(User).filter((User.username == username) | (User.email == email)).first()
            if existing:
                return None

            hashed_pass = User.hash_password(password)

            new_user = User(username=username, email=email, hashed_password=hashed_pass, role=role)

            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            return new_user.id
        except Exception as e:
            if session: session.rollback()
            print(f"Error creating user: {e}")
            return None
        finally:
            if session:
                session.close()

    @staticmethod
    def update_user(user_id: int, email: Optional[str], password: Optional[str]) -> bool:
        session = None
        try:
            session = dbmanager.session
            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                return False

            if email: user.email = email
            if password: user.hashed_password = User.hash_password(password)

            session.commit()
            return True
        except Exception as e:
            if session: session.rollback()
            print(f"Update failed: {e}")
            return False
        finally:
            if session:
                session.close()

    @staticmethod
    def delete_user(user_id: int) -> bool:
        session = None
        try:
            session = dbmanager.session
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                session.delete(user)
                session.commit()
                return True
            return False
        except Exception as e:
            if session: session.rollback()
            print(f"Delete failed: {e}")
            return False
        finally:
            if session:
                session.close()

    @staticmethod
    def send_email(to_email: str, subject: str, body: str):
        email_address = "soccerquiz.suporte@gmail.com"
        email_password = "pqpg uuih evib usrr" 

        msg = EmailMessage()
        msg.set_content(body, subtype='html')
        msg['Subject'] = subject
        msg['From'] = email_address
        msg['To'] = to_email

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(email_address, email_password)
                smtp.send_message(msg)
            print(f"Email enviado para {to_email}")
            return True
        except Exception as e:
            print(f"Falha ao enviar email: {e}")
            return False
        
    @staticmethod
    def password_reset_email(email: str) -> bool:
        token = AuthController.generate_reset_token(email)
        if not token:
            return False
        
        reset_link = f"https://www.youtube.com/"

        subject = "Recuperação de Senha - Soccer Quiz"
        body = f"""
        <html>
            <body>
                <h2>Olá!</h2>
                <p>Recebemos uma solicitação para redefinir sua senha.</p>
                <p>Clique no link abaixo para criar uma nova senha:</p>
                <a href="{reset_link}" style="padding: 10px 20px; background-color: #28a745; color: white; text-decoration: none; border-radius: 5px;">Redefinir Minha Senha</a>
                <p>Este link expira em 15 minutos.</p>
                <p><small>Se não foi você, ignore este e-mail.</small></p>
            </body>
        </html>
        """
        return AuthController.send_email(email, subject, body)
    
    @staticmethod
    def invite_email(to_email: str, inviter_username: str) -> bool:
        register_link = f"https://www.youtube.com/"

        subject = f"{inviter_username} convidou você para o Soccer Quiz!"
        body = f"""
        <html>
            <body>
                <h2>Vem pro jogo! ⚽</h2>
                <p><b>{inviter_username}</b> está te desafiando para ver quem sabe mais sobre futebol.</p>
                <p>Crie sua conta agora e participe dos Quizzes:</p>
                <a href="{register_link}" style="padding: 10px 20px; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px;">Criar Conta Grátis</a>
            </body>
        </html>
        """
        return AuthController.send_email(to_email, subject, body)

    @staticmethod
    def generate_reset_token(email: str) -> Optional[str]:
        session = None
        try:
            session = dbmanager.session
            user = session.query(User).filter(User.email == email).first()
            if not user:
                return None

            payload = {
                "sub": user.username,
                "email": email,
                "type": "reset",
                "exp": datetime.utcnow() + timedelta(minutes=15)
            }

            return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        finally:
            if session:
                session.close()

    @staticmethod
    def reset_password(token: str, new_password: str) -> bool:
        session = None
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            if payload.get("type") != "reset":
                return False

            email = payload.get("email")
            session = dbmanager.session
            user = session.query(User).filter(User.email == email).first()

            if user:
                user.hashed_password = User.hash_password(new_password)
                session.commit()
                return True
            return False
        except Exception as e:
            print(f"Reset error: {e}")
            return False
        finally:
            if session:
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
    def create_tokens(username: str, user_id: int, role: str) -> dict:
        token_jti = str(uuid.uuid4())
        access_payload = {
            "sub": username,
            "id": user_id,
            "role": role,
            "type": "access",
            "jti": token_jti,
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        }
        access_token = jwt.encode(access_payload, SECRET_KEY, algorithm=ALGORITHM)
        refresh_payload = {
            "sub": username,
            "id": user_id,
            "role": role,
            "type": "refresh",
            "jti": token_jti,
            "exp": datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        }
        refresh_token = jwt.encode(refresh_payload, SECRET_KEY, algorithm=ALGORITHM)
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer" }
    
    @staticmethod
    def refresh_access_token(refresh_token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
            if payload.get("type") != "refresh":
                return None
            jti = payload.get("jti")
            if AuthController.is_jti_blacklisted(jti):
                return None
            role = payload.get("role", "user")
            new_access_payload = {
                "sub": payload["sub"],
                "id": payload["id"],
                "role": role,
                "type": "access",
                "jti": jti,
                "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            }
            new_access_token = jwt.encode(new_access_payload, SECRET_KEY, algorithm=ALGORITHM)
            return {"access_token": new_access_token}
        except Exception as e:
            print(f"Error refreshing token: {e}")
            return None

    @staticmethod
    def revoke_token(token: str) -> bool:
        session = None
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            jti = payload.get("jti")
            session = dbmanager.session
            if session.query(TokenBlockList).filter_by(jti=jti).first():
                return True
            block = TokenBlockList(jti=jti)
            session.add(block)
            session.commit()
            return True
        except Exception as e:
            print(f"Error revoking token: {e}")
            return False
        finally:
            if session:
                session.close()

    @staticmethod
    def is_jti_blacklisted(jti: str) -> bool:
        session = None
        try:
            session = dbmanager.session
            exists = session.query(TokenBlockList).filter_by(jti=jti).first()
            return exists is not None
        except Exception as e:
            print(f"Error checking blocklist: {e}")
            return False
        finally:
            if session:
                session.close()