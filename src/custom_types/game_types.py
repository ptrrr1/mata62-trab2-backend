from pydantic import BaseModel

class AnswerPlay(BaseModel):
    id: int
    text: str
    is_correct: bool

class QuestionPlay(BaseModel):
    id: int
    text: str
    answers: list[AnswerPlay]