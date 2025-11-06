import logging

from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker

from model import models

logger = logging.getLogger(__name__)
Base = models.Base


class DBManager:
    def __init__(self):
        logger.info("Initializing Database")

        # TODO: Move to .env file
        self._user = "soccer_u"
        self._password = "soccer_p"
        self._host = "localhost"
        self._port = "3306"
        self._database = "soccer_quiz"

        self._engine = None
        self._session_factory = None
        self._init_engine()

    def _init_engine(self):
        try:
            conn = (
                f"mysql+pymysql://{self._user}:{self._password}@"
                f"{self._host}:{self._port}/{self._database}"
            )

            self._engine = create_engine(conn)
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
