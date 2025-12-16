import logging
from fastapi import APIRouter, Depends
from views.auth_view import get_current_user
from controllers.ranking_controller import RankingController
from custom_types.ranking_types import QuizRanking, GlobalRankingEntry

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/ranking", tags=["Rankings"])

@router.get("/quiz/{quiz_id}", response_model=list[QuizRanking], summary="Ranking do Quiz")
def get_quiz_ranking(quiz_id: int, current_user: dict = Depends(get_current_user)):
    
    data = RankingController.get_quiz_ranking(quiz_id)

    response = []
    
    for index, item in enumerate(data):
        dto = QuizRanking(
            position=index + 1,
            username=item['username'],             
            score=item['score'],
            total_time_seconds=item['duration'],  
            end_time=item['end_time']
        )
        response.append(dto)

    return response

@router.get("/global", response_model=list[GlobalRankingEntry], summary="Ranking Geral")
def get_global_ranking(current_user: dict = Depends(get_current_user)):
    # Chama o Controller
    data = RankingController.get_global_ranking()

    response = []
    
    for index, row in enumerate(data):
        dto = GlobalRankingEntry(
            position=index + 1,
            username=row.username,         
            total_score=row.total_score,
            quizzes_played=row.quizzes_played
        )
        response.append(dto)

    return response