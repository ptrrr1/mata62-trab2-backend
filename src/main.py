import logging
from fastapi import FastAPI

from views import team_view, session_view, answer_view, auth_view

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="logs/debug.log",
    encoding="utf-8",
    format="%(asctime)s %(name)s[%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
    level=logging.INFO,
)

app = FastAPI(title="Soccer-Quiz", root_path="/api/v1")

# Routers are used to organize related views
app.include_router(team_view.router)
app.include_router(session_view.router)
app.include_router(answer_view.router)
app.include_routher(auth_view.router)
