import logging
from fastapi import APIRouter, Depends

from controllers.ranking_controller import RankingController
from custom_types.dashboard_types import QuestionStats
from views.auth_view import admin_access_required

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get(
    "/questions", 
    response_model=list[QuestionStats], 
    summary="Dashboard: Estatísticas de acerto por questão"
)
def get_questions_stats(quiz_id: int = None, current_user: dict = Depends(admin_access_required)):
    stats = RankingController.get_questions_dashboard(quiz_id)
    return stats