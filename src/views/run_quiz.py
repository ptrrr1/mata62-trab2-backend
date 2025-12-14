import logging
from fastapi import APIRouter, HTTPException
from controllers.question_controller import QuestionController
from src.custom_types.user_answers import UserAnswerResponse
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
router = APIRouter(prefix="", tags=["Run Quiz"])


@router.post(
    "/start_quiz/{user_id}/{quiz_id}",
    response_model=StartQuizUnifiedResponse,
    summary="Start a quiz session for a user",
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
    "/finish_quiz/{session_id}",
    response_model=int,
    summary="Finish the quiz and get the score",
)
def finish_quiz(session_id):
    session.end_session(session_id)
    correct_answers = UserAnswerController.get_correct_answers_by_session(session_id)
    score = calculate_score(correct_answers)
    return score


