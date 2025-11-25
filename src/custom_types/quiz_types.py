from pydantic import BaseModel
 
class QuizResponse(BaseModel):
    id: int | None = None
    team_id: int
    is_active: bool

class QuizRequest(BaseModel):
    team_id: int
    is_active: bool