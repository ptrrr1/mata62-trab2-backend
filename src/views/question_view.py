import logging

from fastapi import APIRouter, HTTPException, status

from controllers.question_controller import QuestionController
from custom_types.question_types import Question

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/question", tags=["Questions"])


@router.get(
    "/qid/{id}",
    response_model=list[Question],
    summary="Get questions by id",
)
def get_question_by_id(qid: int):
    response = QuestionController.get_question_id(qid)

    if not response:
        return []

    return response


@router.get(
    "/allquestions",
    response_model=list[Question],
    summary="Get all questions",
)
def get_question_all():
    response = QuestionController.get_question_all()

    if not response:
        return []

    return [
        Question(id=t.id, quiz_id=t.quiz_id, text=t.text, is_active=t.is_active)
        for t in response
    ]


@router.post("/", status_code=status.HTTP_201_CREATED, summary="Create an question")
def create_question(question: Question):
    response = QuestionController.create_question(question)

    if not response:
        raise HTTPException(status_code=400, detail="Failed to create question")

    return dict(message="question created successfully", id=response)


@router.patch("/id/{id}", summary="Update an question")
def patch_question(id: int, question: Question):
    response = QuestionController.patch_question(id, question)

    if not response:
        raise HTTPException(status_code=404, detail="question not found")

    return dict(message="question updated successfully")


@router.delete("/id/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(id: int):
    response = QuestionController.delete_question(id)

    if not response:
        raise HTTPException(status_code=404, detail="question not found")
