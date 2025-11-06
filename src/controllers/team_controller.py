import logging
from typing import Optional

from sqlalchemy import select, insert, update, delete

from custom_types.team_types import TeamRequest
from model import dbmanager
from model.models import Team

logger = logging.getLogger(__name__)


class TeamController:
    @staticmethod
    def get_team_all() -> list:
        s = dbmanager.session
        try:
            q = select(Team)

            return s.scalars(q).all()
        except Exception as e:
            logger.error(f"Failed to fetch teams: {e}")

            return []

    @staticmethod
    def get_team_id(id: int) -> list:
        s = dbmanager.session
        try:
            q = select(Team).where(Team.id == id)

            return s.scalar(q)
        except Exception as e:
            logger.error(f"Failed to fetch team: {e}")

            return None

    @staticmethod
    def create_team(t: TeamRequest) -> Optional[int]:
        s = dbmanager.session
        try:
            q = insert(Team).values(name=t.name)

            r = s.execute(q)
            s.commit()
            
            return r.inserted_primary_key[0]
        except Exception as e:
            logger.error(f"Failed to create team {t}: {e}")
            s.rollback()

            return None

    @staticmethod
    def patch_team(id: str, t: TeamRequest) -> bool:
        s = dbmanager.session
        try:
            q = update(Team).where(Team.id == id).values(name=t.name)
            r = s.execute(q)
            s.commit()

            return r.rowcount > 0
        except Exception as e:
            logger.error(f"Failed to update {id}: {e}")
            
            return False

    @staticmethod
    def delete_team(id: str) -> bool:
        s = dbmanager.session
        try:
            q = delete(Team).where(Team.id == id)

            r = s.execute(q)
            s.commit()

            return r.rowcount > 0
        except Exception as e:
            logger.error(f"Failed to delete {id}: {e}")

            return False
