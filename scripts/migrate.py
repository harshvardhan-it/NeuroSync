from alembic import command
from alembic.config import Config
from sqlalchemy import inspect

from backend.config.settings import settings


def main():
    config = Config("alembic.ini")
    config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

    inspector = inspect(settings.DATABASE_URL if False else __import__("backend.utils.database", fromlist=["engine"]).engine)

    tables = set(inspector.get_table_names())
    if "user" in tables and "dataset" in tables and "alembic_version" not in tables:
        # The pre-Alembic app created the current schema with SQLModel.create_all().
        # Verify the expected columns before stamping so an incompatible schema fails.
        user_columns = {c["name"] for c in inspector.get_columns("user")}
        dataset_columns = {c["name"] for c in inspector.get_columns("dataset")}
        if {"id", "name", "email", "password"} <= user_columns and {
            "id", "user_id", "filename", "file_type", "analysis_result"
        } <= dataset_columns:
            command.stamp(config, "head")
            return

        raise RuntimeError("Existing database schema is incompatible with the initial migration.")

    command.upgrade(config, "head")


if __name__ == "__main__":
    main()
