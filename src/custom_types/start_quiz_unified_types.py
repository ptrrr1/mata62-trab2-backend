from pydantic import BaseModel
from datetime import datetime

class StartQuizUnifiedResponse(BaseModel):
    session_id: int
    quiz_id: int
    start_time: datetime
    end_time: datetime | None = None
    is_active: bool
    