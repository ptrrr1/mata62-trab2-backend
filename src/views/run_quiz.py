import logging
from typing import Union

from fastapi import APIRouter, HTTPException
from controllers.question_controller import QuestionController
from custom_types.answer_types import AnswerResponse
from src.custom_types.user_answers import UserAnswerResponse
from src.custom_types.question_types import QuestionResponse
from src.custom_types.start_quiz_unified_types import StartQuizUnifiedResponse
from src.utils.utils import calculate_score, check_answer
from src.controllers.session_controller import SessionController
from controllers.quiz_controller import QuizController
from src.controllers.user_answers import UserAnswerController
from src.custom_types.user_answers import UserAnswerResponse
 

session = SessionController()
quiz_service = QuizController()
question_controller = QuestionController()
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/run_quiz", tags=["Run Quiz"])


@router.post(
    "/{id}",
    response_model=StartQuizUnifiedResponse,
    summary="Get all questions for a given quiz",
)
def start_quiz(user_id, quiz_id):
    session_obj = session.get_session_by_id_user_and_quiz(user_id, quiz_id)
    if session_obj:
        raise ValueError("Session already exists for this user and quiz")
    else:
        session_obj = session.start_session(
            quiz_id,
            user_id,
        )
        session_obj = session.get_session_by_id(session_obj.id)
        quiz = quiz_service.get_quiz_id(quiz_id)
        print("get_quiz_id func:", quiz_service.get_quiz_id)
        print("module:", quiz_service.get_quiz_id.__module__)

    print("ss_obj", session_obj)

    return StartQuizUnifiedResponse(
        session_id=session_obj.id,
        quiz_id=quiz_id,
        start_time=session_obj.start_time,
        end_time=session_obj.end_time,
        is_active=quiz.is_active,
    )


@router.post(
    "/submit_answer/{question_id}",
    response_model=UserAnswerResponse,
    summary="Get all questions for a given quiz",
)
def submit_answer(question_id, session_id, answer):
    result = check_answer(question_id, int(answer))

    print("result", result)
    check_answer_alredy_exists = UserAnswerController.get_by_session_and_question(
        session_id, question_id
    )
    if check_answer_alredy_exists:
        raise HTTPException(
            status_code=400, detail="Resposta já submetida para esta questão"
        )
    else:
        response = UserAnswerController(
            session_id, question_id, answer, is_correct=result
        )
    response = response.save()
    return response


@router.post(
    "/finish_quiz/{session_id}",
    response_model=int,
    summary="Finish the quiz and get the score",
)
def finish_quiz(session_id):
    session.end_session(session_id)
    correct_answers = UserAnswerController.get_correct_answers_by_session(session_id)
    score = calculate_score(correct_answers)
    return score


@router.get(
    "get_all_answers/{session_id}",
    response_model=list[UserAnswerResponse],
    summary="Get all answers for a given session",
)
def get_all_answers(session_id, quiz_id):
    answers = UserAnswerController.get_by_session_and_quiz(int(session_id), int(quiz_id))
    return answers
