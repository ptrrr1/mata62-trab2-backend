import logging
from typing import Optional

from sqlalchemy import select, insert, update, delete

from custom_types.answer_types import AnswerRequest
from model import dbmanager
from model.models import Answer

logger = logging.getLogger(__name__)


class AnswerController:
    @staticmethod
    def get_answers_by_question(qid) -> list[Answer]:
        s = dbmanager.session
        try:
            q = select(Answer).where(Answer.question_id == qid)

            return s.scalars(q).all()
        except Exception as e:
            logger.error(f"Failed to fetch answers: {e}")

            return []

    @staticmethod
    def create_answer(answer: AnswerRequest) -> Optional[int]:
        s = dbmanager.session
        try:
            q = insert(Answer).values(
                question_id=answer.question_id,
                text=answer.text,
                is_correct=answer.is_correct,
            )
            r = s.execute(q)
            s.commit()

            return r.inserted_primary_key[0]
        except Exception as e:
            logger.error(f"Failed to create answer: {e}")
            s.rollback()

            return None

    @staticmethod
    def patch_answer(id: int, answer: AnswerRequest) -> bool:
        s = dbmanager.session
        try:
            q = (
                update(Answer)
                .where(Answer.id == id)
                .values(
                    question_id=answer.question_id,
                    text=answer.text,
                    is_correct=answer.is_correct,
                )
            )
            r = s.execute(q)
            s.commit()

            return r.rowcount > 0
        except Exception as e:
            logger.error(f"Failed to patch answer: {e}")
            s.rollback()

            return False

    @staticmethod
    def delete_answer(id: int) -> bool:
        s = dbmanager.session
        try:
            q = delete(Answer).where(Answer.id == id)
            r = s.execute(q)
            s.commit()

            return r.rowcount > 0
        except Exception as e:
            logger.error(f"Failed to patch answer: {e}")
            s.rollback()

            return False
