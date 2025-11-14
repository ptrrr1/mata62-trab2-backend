import logging
from typing import Optional

from sqlalchemy import insert, null, select, update, func

from custom_types.session_types import SessionStart
from model import dbmanager
from model.models import Session

logger = logging.getLogger(__name__)


class SessionController:
    @staticmethod
    def get_session_all() -> list[Session]:
        s = dbmanager.session
        try:
            q = select(Session).where(Session.end_time == null())

            return s.scalars(q).all()
        except Exception as e:
            logger.error(f"Failed to fetch active sessions: {e}")

            return []

    @staticmethod
    def start_session(t: SessionStart) -> Optional[int]:
        s = dbmanager.session
        try:
            # q = insert(Session).values(quiz_id=t.quiz_id, user_id=t.user_id)
            q = insert(Session).values(quiz_id=t.quiz_id)

            r = s.execute(q)
            s.commit()

            return r.inserted_primary_key[0]
        except Exception as e:
            logger.error(f"Failed to create team {t}: {e}")
            s.rollback()

            return None

    @staticmethod
    def end_session(id: int) -> bool:
        s = dbmanager.session
        try:
            q = (
                update(Session)
                .where(Session.id == id)
                .values(end_time=func.current_timestamp())
            )
            r = s.execute(q)
            s.commit()

            return r.rowcount > 0
        except Exception as e:
            logger.error(f"Failed to update {id}: {e}")
            s.rollback()

            return False

    # @staticmethod
    # def delete_session(id: int) -> bool:
    #     s = dbmanager.session
    #     try:
    #         q = update(Session).where(Session.id == id).values(is_active=False)

    #         r = s.execute(q)
    #         s.commit()

    #         return r.rowcount > 0
    #     except Exception as e:
    #         logger.error(f"Failed to delete {id}: {e}")

    #         return False
