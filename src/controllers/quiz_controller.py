import logging
from typing import Optional

from sqlalchemy import select, insert, update

from custom_types.quiz_types import QuizType
from model import dbmanager
from model.models import Quiz

logger = logging.getLogger(__name__)


class QuizController:
    @staticmethod
    def get_quiz_all() -> list[Quiz]:
        s = dbmanager.session
        try:
            q = select(Quiz)

            return s.scalars(q).all()
        except Exception as e:
            logger.error(f"Failed to fetch Quizs: {e}")

            return []

    @staticmethod
    def get_quiz_id(id: int) -> list:
        s = dbmanager.session
        try:
            logger.info(f"printando{id}")
            q = select(Quiz).where(Quiz.id == id)
            logger.info(f"printandoq{q}")

            return s.scalars(q).all()
        except Exception as e:
            logger.error(f"Failed to fetch Quiz: {e}")

            return None

    @staticmethod
    def create_quiz(t: QuizType) -> Optional[int]:
        s = dbmanager.session
        try:
            q = insert(Quiz).values(
                team_id=t.team_id,
                is_active=t.is_active,
            )

            r = s.execute(q)
            s.commit()

            return r.inserted_primary_key[0]
        except Exception as e:
            logger.error(f"Failed to create Quiz {t}: {e}")
            s.rollback()

            return None

    @staticmethod
    def patch_quiz(id: int, t: Quiz) -> bool:
        s = dbmanager.session
        try:
            q = (
                update(Quiz)
                .where(Quiz.id == id)
                .values(team_id=t.team_id, is_active=t.is_active)
            )
            r = s.execute(q)
            s.commit()

            return r.rowcount > 0
        except Exception as e:
            logger.error(f"Failed to update {id}: {e}")
            s.rollback()

            return False

    @staticmethod
    def delete_quiz(id: int) -> bool:
        s = dbmanager.session
        try:
            q = update(Quiz).where(Quiz.id == id).values(is_active=False)

            r = s.execute(q)
            s.commit()

            return r.rowcount > 0
        except Exception as e:
            logger.error(f"Failed to delete {id}: {e}")
            s.rollback()

            return False
