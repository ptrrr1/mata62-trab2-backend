
from typing import Optional
from pydantic import BaseModel

class Question(BaseModel):
    id: Optional[int] = None
    quiz_id: int
    is_active: bool
    text: str



 

