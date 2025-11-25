import logging
import os
import sys
from fastapi import FastAPI

from views import team_view, session_view, answer_view, auth_view

# Configure logging
# logger = logging.getLogger(__name__)
# os.makedirs("logs", exist_ok=True)
# logging.basicConfig(
#     filename="logs/debug.log",
#     encoding="utf-8",
#     format="%(asctime)s %(name)s[%(levelname)s]: %(message)s",
#     datefmt="%Y-%m-%dT%H:%M:%S",
#     level=logging.INFO,
# )
logging.basicConfig(
    level=logging.DEBUG,  # Define o nível de log
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)  # Envia logs para o stdout
    ]
)

logger = logging.getLogger(__name__)

logger.info("Logging configurado para o container")

app = FastAPI(title="Soccer-Quiz", root_path="/api/v1")

# Routers are used to organize related views
app.include_router(team_view.router)
app.include_router(session_view.router)
app.include_router(answer_view.router)
app.include_router(auth_view.router)
