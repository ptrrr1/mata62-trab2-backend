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
    def get_session_by_id(id: int) -> Optional[Session]:
        s = dbmanager.session
        try:
            q = select(Session).where(Session.id == id)

            return s.scalar(q)
        except Exception as e:
            logger.error(f"Failed to fetch session: {e}")

            return None
    @staticmethod
    def get_session_by_id_user_and_quiz(user_id: int, quiz_id: int) -> Optional[Session]:
        s = dbmanager.session
        print('teste controller get_session_by_id_user_and_quiz',user_id,quiz_id)
        try:
            q = select(Session).where(Session.user_id == user_id and Session.quiz_id == quiz_id)

            return s.scalar(q)
        except Exception as e:
            logger.error(f"Failed to fetch session: {e}")

            return None
          
    @staticmethod
    def start_session(quiz_id, user_id: int) -> Session:
        s = dbmanager.session
        print('teste controller',quiz_id,user_id)
        try:
            session = Session(
                user_id=user_id,
                quiz_id=quiz_id,
            )
            s.add(session)
            s.commit()
            s.refresh(session)   

            return session
        except Exception as e:
            s.rollback()
            logger.error(f"Failed to create session {quiz_id}, {user_id}: {e}")
            raise

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
