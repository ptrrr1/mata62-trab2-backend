import logging

from fastapi import APIRouter, HTTPException, status

from controllers.session_controller import SessionController
from custom_types.session_types import SessionResponse, SessionStart

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/session", tags=["Sessions"])


@router.get(
    "/all", response_model=list[SessionResponse], summary="Get all active sessions"
)
def get_session_all():
    response = SessionController.get_session_all()

    if not response:
        return []

    return [
        SessionResponse(
            id=t.id, quiz_id=t.quiz_id, start_time=t.start_time, end_time=t.end_time
        )
        for t in response
    ]


# TODO: Active Session by user id
# TODO: Session by id (get status, if active or not)


@router.post("/", status_code=status.HTTP_201_CREATED, summary="Start a session")
def start_session(session: SessionStart):
    response = SessionController.start_session(session)

    if not response:
        raise HTTPException(status_code=400, detail="Failed to start session")

    return dict(message="Session started successfully", id=response)


@router.patch("/id/{id}", summary="End a session")
def end_session(id: int):
    response = SessionController.end_session(id)

    if not response:
        raise HTTPException(status_code=400, detail="Failed to end session")

    return dict(message="Session ended successfully")


# @router.delete("/id/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_team(id: int):
#     response = SessionController.delete_session(id)

#     if not response:
#         raise HTTPException(status_code=404, detail="Session not found")

#     return dict(message="Session deleted successfully")
