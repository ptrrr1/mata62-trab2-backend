from pydantic import BaseModel


class TeamResponse(BaseModel):
    id: int
    name: str


class TeamRequest(BaseModel):
    name: str
