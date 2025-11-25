from pydantic import BaseModel


class AnswerResponse(BaseModel):
    id: int
    text: str
    is_correct: bool


class AnswerRequest(BaseModel):
    question_id: int
    text: str
    is_correct: bool
