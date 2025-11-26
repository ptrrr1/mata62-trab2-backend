import logging

from fastapi import APIRouter, HTTPException, status, Depends

from controllers.answer_controller import AnswerController
from custom_types.answer_types import AnswerResponse, AnswerRequest
from views.auth_view import get_current_user, admin_access_required

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/answer", tags=["Answers"])


@router.get(
    "/qid/{id}",
    response_model=list[AnswerResponse],
    summary="Get all answers for a given question",
)
def get_answers_by_question(qid: int):
    response = AnswerController.get_answers_by_question(qid)

    if not response:
        return []

    return [AnswerResponse(id=t.id, text=t.text) for t in response]


@router.post("/", status_code=status.HTTP_201_CREATED, summary="Create an answer")
def create_answer(answer: AnswerRequest, current_user: dict = Depends(admin_access_required)):
    response = AnswerController.create_answer(answer)

    if not response:
        raise HTTPException(status_code=400, detail="Failed to create answer")

    return dict(message="Answer created successfully", id=response)


@router.patch("/id/{id}", summary="Update an answer")
def patch_answer(id: int, answer: AnswerRequest,
                 current_user: dict = Depends(admin_access_required)):
    response = AnswerController.patch_answer(id, answer)

    if not response:
        raise HTTPException(status_code=404, detail="Answer not found")

    return dict(message="Answer updated successfully")


@router.delete("/id/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_answer(id: int, current_user: dict = Depends(admin_access_required)):
    response = AnswerController.delete_answer(id)

    if not response:
        raise HTTPException(status_code=404, detail="Answer not found")

    return dict(message="Answer deleted successfully")
