import logging

from fastapi import APIRouter, HTTPException, status

from controllers.quiz_controller import QuizController
from custom_types.quiz_types import QuizRequest, QuizResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/quiz", tags=["Quizzes"])


@router.get(
    "/qid/{id}",
    response_model=list[QuizResponse],
    summary="Get quiz by id",
)
def get_quiz_by_quiz(qid: int):
    response = QuizController.get_quiz_id(qid)

    if not response:
        return []

    return [
        QuizResponse(id=t.id, team_id=t.team_id, is_active=t.is_active) for t in response
    ]

@router.get(
    "/all", response_model=list[QuizResponse], summary="Get all quizzes"
)
def get_quiz_all():
    response = QuizController.get_quiz_all()

    if not response:
        return []

    return [
        QuizResponse(id=t.id, team_id=t.team_id, is_active=t.is_active) for t in response
    ]

@router.get(
    "/team/{team_id}",
    response_model=list[QuizResponse],
    summary="Get quiz by Team ID"
)
def get_quiz_all_by_team(team_id: int):
    response = QuizController.get_quiz_all_by_team_id(team_id)

    if not response:
        return []
    
    return [
        QuizResponse(id=t.id, team_id=t.team_id, is_active=t.is_active) for t in response
    ]

@router.post("/", status_code=status.HTTP_201_CREATED, summary="Create an quiz")
def create_quiz(quiz: QuizRequest):
    response = QuizController.create_quiz(quiz)

    if not response:
        raise HTTPException(status_code=400, detail="Failed to create quiz")

    return dict(message="quiz created successfully", id=response)


@router.patch("/id/{id}", summary="Update an quiz")
def patch_quiz(id: int, quiz: QuizRequest):
    response = QuizController.patch_quiz(id, quiz)

    if not response:
        raise HTTPException(status_code=404, detail="quiz not found")

    return dict(message="quiz updated successfully")


@router.delete("/id/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quiz(id: int):
    response = QuizController.delete_quiz(id)

    if not response:
        raise HTTPException(status_code=404, detail="quiz not found")

    return dict(message="quiz deleted successfully")
