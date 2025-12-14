from datetime import datetime
from pydantic import BaseModel

class UserAnswerResponse(BaseModel):
    session_id: int
    question_id: int
    answer_id: int
    created_at: datetime