import logging

from fastapi import APIRouter, HTTPException, status

from controllers.quiz_controller import QuizController
from custom_types.quiz_types import QuizType

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/quiz", tags=["Quizzes"])


@router.get(
    "/qid/{id}",
    response_model=list[QuizType],
    summary="Get all quizs for a given quiz",
)
def get_quiz_by_quiz(qid: int):
    response = QuizController.get_quiz_id(qid)

    if not response:
        return []

    return [
        QuizType(id=t.id, team_id=t.team_id, is_active=t.is_active) for t in response
    ]


@router.post("/", status_code=status.HTTP_201_CREATED, summary="Create an quiz")
def create_quiz(quiz: QuizType):
    response = QuizController.create_quiz(quiz)

    if not response:
        raise HTTPException(status_code=400, detail="Failed to create quiz")

    return dict(message="quiz created successfully", id=response)


@router.patch("/id/{id}", summary="Update an quiz")
def patch_quiz(id: int, quiz: QuizType):
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
