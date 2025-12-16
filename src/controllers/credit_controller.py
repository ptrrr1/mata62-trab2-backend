import logging

from sqlalchemy import select, insert, update

from model import dbmanager
from model.models import User, CreditsRegistry

logger = logging.getLogger(__name__)


class CreditController:
    @staticmethod
    def get_user_credits(id: int) -> int:
        s = dbmanager.session
        try:
            q = select(User.credits).where(User.id == id)

            return s.scalars(q).first()
        except Exception as e:
            logger.error(f"Failed to fetch user credit amount: {e}")

            return None

    @staticmethod
    def get_user_credits_history(id: int) -> list:
        s = dbmanager.session
        try:
            q = (
                select(CreditsRegistry)
                .where(CreditsRegistry.user_id == id)
                .order_by(CreditsRegistry.created_at.desc())
            )

            return s.scalars(q).all()
        except Exception as e:
            logger.error(f"Failed to fetch user credit history: {e}")

            return None

    @staticmethod
    def get_all_credits_history() -> list:
        s = dbmanager.session
        try:
            q = (
                select(CreditsRegistry)
                .order_by(CreditsRegistry.created_at.desc())
                .limit(100)
            )

            return s.scalars(q).all()
        except Exception as e:
            logger.error(f"Failed to fetch credit history: {e}")

            return None

    @staticmethod
    def create_buy_request(user_id: int, amount: int) -> bool:
        if amount <= 0:
            return False

        s = dbmanager.session
        try:
            with s.begin():
                u = (
                    update(User)
                    .where(User.id == user_id)
                    .values(credits=User.credits + amount)
                )
                r = s.execute(u)

                if r.rowcount == 0:
                    raise ValueError(f"User{user_id} was not found")

                q = insert(CreditsRegistry).values(amount=amount, user_id=user_id)
                r = s.execute(q)

            return True
        except Exception as e:
            logger.error(f"Failed to create buy request: {e}")

            return False

    @staticmethod
    def use_credit(user_id: int, amount: int) -> bool:
        if amount <= 0:
            return False

        s = dbmanager.session
        try:
            u = (
                update(User)
                .where(User.id == user_id, User.credits >= amount)
                .values(credits=User.credits - amount)
            )
            r = s.execute(u)
            s.commit()

            return r.rowcount > 0
        except Exception as e:
            logger.error(f"Failed to use credits: {e}")

            return False
