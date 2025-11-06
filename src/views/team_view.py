import logging
from fastapi import APIRouter, HTTPException, status

from controllers.team_controller import TeamController
from custom_types.team_types import TeamRequest, TeamResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/team", tags=["Teams"])


@router.get("/all", response_model=list[TeamResponse])
def get_team_all():
    response = TeamController.get_team_all()

    if not response:
        return []

    return map(lambda t: TeamResponse(id=t.id, name=t.name), response)


@router.get("/id/{id}", response_model=TeamResponse)
def get_team_id(id: int) -> TeamResponse:
    response = TeamController.get_team_id(id)

    if not response:
        raise HTTPException(status_code=404, detail="Team not found")

    return TeamResponse(id=response.id, name=response.name)


@router.post("/", status_code=status.HTTP_201_CREATED)
def post_team(team: TeamRequest):
    response = TeamController.create_team(team)

    if not response:
        raise HTTPException(status_code=400, detail="Failed to create Team")

    return dict(message="Team created successfully")


@router.patch("/id/{id}")
def patch_team(id: int, team: TeamRequest):
    response = TeamController.patch_team(id, team)

    if not response:
        raise HTTPException(status_code=404, detail="Team not found")

    return dict(message="Team updated successfully")


@router.delete("/id/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_team(id: int):
    response = TeamController.delete_team(id)

    if not response:
        raise HTTPException(status_code=404, detail="Team not found")

    return dict(message="Team deleted successfully")
