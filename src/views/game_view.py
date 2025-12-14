import logging
from fastapi import APIRouter, HTTPException

from controllers.question_controller import QuestionController
from custom_types.game_types import QuestionPlay, AnswerPlay

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/game", tags=["Game Play"])

@router.get("/play/team/{team_id}", response_model=list[QuestionPlay], summary="Get full quiz data for a team")
def get_game_data(team_id: int):
    questions_db = QuestionController.get_full_quiz_by_team(team_id)
    
    if not questions_db:
        return []

    result = []
    for q in questions_db:
        answers_list = [
            AnswerPlay(id=a.id, text=a.text, is_correct=a.is_correct) 
            for a in q.answers
        ]
        
        result.append(QuestionPlay(id=q.id, text=q.text, answers=answers_list))
        
    return result