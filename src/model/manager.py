import logging
import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from model import models

logger = logging.getLogger(__name__)
Base = models.Base


class DBManager:
    def __init__(self):
        logger.info("Initializing Database")
        self._database_url = os.getenv("DATABASE_URL")

        if not self._database_url:
            self._user = os.getenv("DB_USER", "soccer_u")
            self._password = os.getenv("DB_PASSWORD", "soccer_p")
            self._host = os.getenv("DB_HOST", "db")
            self._port = os.getenv("DB_PORT", "3306")
            self._database = os.getenv("DB_NAME", "soccer_quiz")
        else:
            self._user = None
            self._password = None
            self._host = None
            self._port = None
            self._database = None

        self._engine = None
        self._session_factory = None
        self._init_engine()

    def _init_engine(self):
        try:
            if self._database_url:
                conn = self._database_url
            else:
                from urllib.parse import quote_plus

                pwd = quote_plus(self._password) if self._password else ""
                conn = (
                    f"mysql+pymysql://{self._user}:{pwd}@"
                    f"{self._host}:{self._port}/{self._database}"
                )

            self._engine = create_engine(conn, pool_pre_ping=True)
            self._session_factory = sessionmaker(
                bind=self._engine, autocommit=False, autoflush=False
            )

            logger.info("Database engine initialized")

        except Exception as e:
            logger.error(f"Failed to initialize database engine: {e}")
            raise

    @property
    def session(self):
        if not self._session_factory:
            raise RuntimeError("Database engine not intialized")

        return self._session_factory()

    def create_tables(self, base=Base):
        try:
            base.metadata.create_all(self._engine)
            logger.info("Tables created")

        except Exception as e:
            logger.error(f"Failed to create tables: {e}")
            raise

    def test_conn(self):
        try:
            self.session.execute(text("SHOW TABLES;"))
            logger.info("Database connected")

            return True
        except Exception as e:
            logger.error(f"Failed to connect to Database: {e}")

            return False
