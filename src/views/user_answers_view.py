
from fastapi import APIRouter, HTTPException

from controllers.user_answers import UserAnswerController
from custom_types.user_answers import UserAnswerResponse
from utils.utils import check_answer

router = APIRouter(prefix="", tags=["User Answers"])

@router.get(
    "/get_all_answers/{session_id}",
    response_model=list[UserAnswerResponse],
    summary="Get all answers for a given session",
)
def get_all_answers(session_id, quiz_id):
    answers = UserAnswerController.get_by_session_and_quiz(
        int(session_id), int(quiz_id)
    )
    return answers

@router.post(
    "/submit_answer/{question_id}",
    response_model=UserAnswerResponse,
    summary="submit an answer for a question",
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
