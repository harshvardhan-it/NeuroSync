from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy import text

from backend.config.settings import settings
from backend.utils.logger import logger


engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

    # Lightweight idempotent indexes for deployments without Alembic yet.
    with engine.begin() as connection:
        try:
            connection.execute(
                text("CREATE INDEX IF NOT EXISTS ix_dataset_user_id ON dataset (user_id)")
            )
        except Exception:
            logger.exception("Could not create dataset ownership index.")

        try:
            connection.execute(
                text("CREATE UNIQUE INDEX IF NOT EXISTS uq_user_email ON user (email)")
            )
        except Exception:
            logger.exception(
                "Could not create unique user email index. Existing duplicate emails may require cleanup."
            )


def get_session():
    with Session(engine) as session:
        yield session
