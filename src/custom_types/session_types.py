from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class SessionResponse(BaseModel):
    id: int
    # user_id: int
    quiz_id: int
    start_time: datetime
    end_time: Optional[datetime]


class SessionStart(BaseModel):
    # user_id: int
    quiz_id: int
