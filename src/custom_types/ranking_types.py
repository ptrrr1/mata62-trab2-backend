from pydantic import BaseModel
from datetime import datetime

class QuizRanking(BaseModel):
    position: int
    username: str
    score: int
    total_time_seconds: float
    end_time: datetime

class GlobalRankingEntry(BaseModel):
    position: int
    username: str
    total_score: int
    quizzes_played: int