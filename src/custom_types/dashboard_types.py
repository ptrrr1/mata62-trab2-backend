from pydantic import BaseModel

class QuestionStats(BaseModel):
    question_id: int
    text: str
    total_attempts: int
    correct_count: int
    wrong_count: int
    accuracy_percent: float