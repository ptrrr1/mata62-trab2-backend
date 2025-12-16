from datetime import datetime
import logging

from fastapi import logger
from model import dbmanager
from model.models import Session, UserAnswer as UserAnswerModel


logger = logging.getLogger(__name__)


class UserAnswerController:

    def __init__(
        self, session_id: int, question_id: int, answer_id: int, is_correct: bool
    ):
        self.session_id = session_id
        self.question_id = question_id
        self.answer_id = answer_id
        self.is_correct = bool(is_correct)

    def save(self) -> UserAnswerModel:
        try:
            self.db = dbmanager.session
            db_answer = UserAnswerModel(
                session_id=self.session_id,
                question_id=self.question_id,
                answer_id=self.answer_id,
                is_correct=self.is_correct,
            )

            self.db.add(db_answer)
            self.db.commit()
            self.db.refresh(db_answer)

            return db_answer

        except Exception:
            self.db.rollback()
            logger.error("Erro ao salvar UserAnswer")
            raise

    @staticmethod
    def get_by_session_and_question(
        session_id: int, question_id: int
    ) -> UserAnswerModel | None:
        try:
            print("teste get_by_session_and_question", session_id, question_id)
            db = dbmanager.session
            user_answer = (
                db.query(UserAnswerModel)
                .filter_by(session_id=session_id, question_id=question_id)
                .first()
            )

            return user_answer

        except Exception:
            logger.error("Erro ao buscar UserAnswer por sessão e questão")
            return None

    staticmethod

    def get_by_session_and_quiz(session_id: int, quiz_id: int) -> list[UserAnswerModel]:
        try:
            db = dbmanager.session
            user_answers = (
                db.query(UserAnswerModel)
                .join(Session, UserAnswerModel.session_id == Session.id)
                .filter(Session.id == session_id, Session.quiz_id == quiz_id)
                .all()
            )

            return user_answers

        except Exception:
            logger.error("Erro ao buscar UserAnswers por sessão e quiz")
            return []

    def get_correct_answers_by_session(session_id: int) -> list[UserAnswerModel]:
        try:
            db = dbmanager.session
            correct_answers = (
                db.query(UserAnswerModel)
                .filter_by(session_id=session_id, is_correct=True)
                .all()
            )

            return correct_answers

        except Exception:
            logger.error("Erro ao buscar respostas corretas por sessão")
            return []
