import logging
from typing import Optional
from sqlalchemy.orm import selectinload

from sqlalchemy import select, insert, update

from custom_types.question_types import QuestionRequest,QuestionResponse
from model import dbmanager
from model.models import Question, Quiz

logger = logging.getLogger(__name__)


class QuestionController:
    @staticmethod
    def get_question_all() -> list[QuestionResponse]:
        s = dbmanager.session
        try:
            q = select(Question)

            return s.scalars(q).all()
        except Exception as e:
            logger.error(f"Failed to fetch Questions: {e}")
            return []
        
    @staticmethod
    def get_full_quiz_by_team(team_id: int) -> list[Question]:
        s = dbmanager.session
        try:
            q = (
                select(Question)
                .join(Quiz, Question.quiz_id == Quiz.id)
                .where(Quiz.team_id == team_id, Question.is_active == True)
                .options(selectinload(Question.answers))
            )
            
            return s.scalars(q).all()
        except Exception as e:
            logger.error(f"Failed to fetch game data for team {team_id}: {e}")
            return []

    @staticmethod
    def get_question_id(id: int) -> list:
        s = dbmanager.session
        try:
            logger.info(f"printando{id}")
            q = select(Question).where(Question.id == id)
            logger.info(f"printandoq{q}")

            return s.scalars(q).all()
        except Exception as e:
            logger.error(f"Failed to fetch Quiz: {e}")

            return None
        
    @staticmethod
    def get_questions_by_quiz_id(quiz_id: int) -> list[QuestionResponse]:
        s = dbmanager.session
        try:
            q = select(Question).where(
                Question.quiz_id == quiz_id,
            )
            return s.scalars(q).all()
        except Exception as e:
            logger.error(f"Failed to fetch questions for quiz {quiz_id}: {e}")
            return []
        
    @staticmethod
    def get_questions_by_team_id(team_id: int) -> list[QuestionResponse]:
        s = dbmanager.session
        try:
            q = (
                select(Question)
                .join(Quiz, Question.quiz_id == Quiz.id)
                .where(
                    Quiz.team_id == team_id,
                )
            )
            return s.scalars(q).all()
        except Exception as e:
            logger.error(f"Failed to fetch questions for team {team_id}: {e}")
            return []

    @staticmethod
    def create_question(t: QuestionRequest) -> Optional[int]:
        s = dbmanager.session
        try:
            q = insert(Question).values(
                quiz_id=t.quiz_id,
                text=t.text,
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
    def patch_question(id: int, t: QuestionRequest) -> bool:
        s = dbmanager.session
        try:
            q = (
                update(Question)
                .where(Question.id == id)
                .values(quiz_id=t.quiz_id, text=t.text, is_active=t.is_active)
            )
            r = s.execute(q)
            s.commit()

            return r.rowcount > 0
        except Exception as e:
            logger.error(f"Failed to update {id}: {e}")
            s.rollback()

            return False

    @staticmethod
    def delete_question(id: int) -> bool:
        s = dbmanager.session
        try:
            q = update(Question).where(Question.id == id).values(is_active=False)

            r = s.execute(q)
            s.commit()

            return r.rowcount > 0
        except Exception as e:
            logger.error(f"Failed to delete {id}: {e}")
            s.rollback()

            return False
