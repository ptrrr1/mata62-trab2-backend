from pydantic import BaseModel
 
class QuizType(BaseModel):
    id: int
    team_id: int
    is_active: bool
