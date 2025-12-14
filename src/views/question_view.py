import logging

from fastapi import APIRouter, HTTPException, status

from controllers.question_controller import QuestionController
from custom_types.question_types import QuestionRequest, QuestionResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/question", tags=["Questions"])


@router.get(
    "/qid/{id}",
    response_model=list[QuestionResponse],
    summary="Get questions by id",
)
def get_question_by_id(id: int): 
    response = QuestionController.get_question_id(id)

    if not response:
        return []

    return response

@router.get("/quiz/{quiz_id}", response_model=list[QuestionResponse], summary="Get all questions for a specific Quiz")
def get_questions_by_quiz(quiz_id: int):
    response = QuestionController.get_questions_by_quiz_id(quiz_id)
    if not response:
        return []
    
    return [
        QuestionResponse(id=t.id, quiz_id=t.quiz_id, text=t.text, is_active=t.is_active)
        for t in response
    ]

# ... imports ...

@router.get(
    "/team/{team_id}", 
    response_model=list[QuestionResponse], 
    summary="Get all questions for a specific Team"
)
def get_questions_by_team(team_id: int):
    response = QuestionController.get_questions_by_team_id(team_id)

    if not response:
        return []

    return [
        QuestionResponse(id=t.id, quiz_id=t.quiz_id, text=t.text, is_active=t.is_active)
        for t in response
    ]

@router.get(
    "/allquestions",
    response_model=list[QuestionResponse],
    summary="Get all questions",
)
def get_question_all():
    response = QuestionController.get_question_all()

    if not response:
        return []

    return [
        QuestionResponse(id=t.id, quiz_id=t.quiz_id, text=t.text, is_active=t.is_active)
        for t in response
    ]


@router.post("/", status_code=status.HTTP_201_CREATED, summary="Create an question")
def create_question(question: QuestionRequest):
    response = QuestionController.create_question(question)

    if not response:
        raise HTTPException(status_code=400, detail="Failed to create question")

    return dict(message="question created successfully", id=response)


@router.patch("/id/{id}", summary="Update an question")
def patch_question(id: int, question: QuestionRequest):
    response = QuestionController.patch_question(id, question)

    if not response:
        raise HTTPException(status_code=404, detail="question not found")

    return dict(message="question updated successfully")


@router.delete("/id/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(id: int):
    response = QuestionController.delete_question(id)

    if not response:
        raise HTTPException(status_code=404, detail="question not found")
