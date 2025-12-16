import logging
import sys
from fastapi import FastAPI

from views import (
    question_view,
    quiz_view,
    team_view,
    session_view,
    answer_view,
    auth_view,
    game_view,
    run_quiz,
    user_answers_view,
    ranking_view,
    credit_view
)
 
logging.basicConfig(
    level=logging.DEBUG,  # Define o nível de log
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],  # Envia logs para o stdout
)

logger = logging.getLogger(__name__)

logger.info("Logging configurado para o container")

app = FastAPI(title="Soccer-Quiz", root_path="/api/v1")

# Routers are used to organize related views
app.include_router(auth_view.router)
app.include_router(team_view.router)
app.include_router(quiz_view.router)
app.include_router(question_view.router)
app.include_router(answer_view.router)
app.include_router(session_view.router)
app.include_router(run_quiz.router)
app.include_router(user_answers_view.router)
app.include_router(game_view.router)
app.include_router(ranking_view.router)
app.include_router(credit_view.router)

