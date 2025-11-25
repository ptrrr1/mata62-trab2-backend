
from typing import Optional
from pydantic import BaseModel

class QuestionResponse(BaseModel):
    id: Optional[int] = None
    quiz_id: int
    is_active: bool
    text: str


class QuestionRequest(BaseModel):
    quiz_id: int
    is_active: bool
    text: str
 

