from alembic import command
from alembic.config import Config
from sqlalchemy import inspect, text

from backend.config.settings import settings
from backend.utils.database import engine


REQUIRED_COLUMNS = {
    "user": {
        "id",
        "name",
        "email",
        "password",
        "focus_score",
        "streak",
    },
    "dataset": {
        "id",
        "user_id",
        "filename",
        "file_type",
        "rows",
        "columns",
        "status",
        "analysis_result",
        "uploaded_at",
    },
    "chatmessage": {
        "id",
        "user_id",
        "dataset_id",
        "role",
        "content",
        "created_at",
    },
}


def validate_existing_schema(inspector):
    tables = set(inspector.get_table_names())

    for table in ("user", "dataset"):
        if table not in tables:
            raise RuntimeError(
                f"Existing database is missing required table: {table}"
            )

        columns = {
            column["name"]
            for column in inspector.get_columns(table)
        }

        missing = REQUIRED_COLUMNS[table] - columns

        if missing:
            raise RuntimeError(
                f"Incompatible {table} schema. Missing columns: {sorted(missing)}"
            )

    if "chatmessage" in tables:
        columns = {
            column["name"]
            for column in inspector.get_columns("chatmessage")
        }

        missing = REQUIRED_COLUMNS["chatmessage"] - columns

        if missing:
            raise RuntimeError(
                "Incompatible chatmessage schema. "
                f"Missing columns: {sorted(missing)}"
            )


def reconcile_legacy_schema():
    """
    Bring the existing pre-Alembic schema in line with migration 0001.

    This function only adds missing constraints and indexes.
    It does not drop or recreate existing tables or records.
    """

    inspector = inspect(engine)
    validate_existing_schema(inspector)

    with engine.begin() as connection:
        # Check email data before enforcing uniqueness.
        duplicate_emails = connection.execute(
            text("""
                SELECT email, COUNT(*)
                FROM "user"
                GROUP BY email
                HAVING COUNT(*) > 1
            """)
        ).fetchall()

        null_emails = connection.execute(
            text("""
                SELECT COUNT(*)
                FROM "user"
                WHERE email IS NULL
            """)
        ).scalar_one()

        if duplicate_emails or null_emails:
            raise RuntimeError(
                "Cannot enforce email uniqueness: duplicate or NULL emails exist."
            )

        # Add the named unique constraint if missing.
        unique_constraints = {
            constraint["name"]
            for constraint in inspector.get_unique_constraints("user")
        }

        if "uq_users_email" not in unique_constraints:
            connection.execute(
                text("""
                    ALTER TABLE "user"
                    ADD CONSTRAINT uq_users_email UNIQUE (email)
                """)
            )

        # Match the unique email index declared in migration 0001.
        connection.execute(
            text("""
                CREATE UNIQUE INDEX IF NOT EXISTS ix_user_email
                ON "user" (email)
            """)
        )

        # Match dataset indexes from migration 0001.
        connection.execute(
            text("""
                CREATE INDEX IF NOT EXISTS ix_dataset_user_id
                ON dataset (user_id)
            """)
        )

        connection.execute(
            text("""
                CREATE INDEX IF NOT EXISTS ix_dataset_filename
                ON dataset (filename)
            """)
        )

        # Preserve existing chatmessage indexes and add only if missing.
        tables = set(inspect(engine).get_table_names())

        if "chatmessage" in tables:
            connection.execute(
                text("""
                    CREATE INDEX IF NOT EXISTS ix_chatmessage_user_id
                    ON chatmessage (user_id)
                """)
            )

            connection.execute(
                text("""
                    CREATE INDEX IF NOT EXISTS ix_chatmessage_dataset_id
                    ON chatmessage (dataset_id)
                """)
            )


def main():
    config = Config("alembic.ini")
    config.set_main_option(
        "sqlalchemy.url",
        settings.DATABASE_URL,
    )

    inspector = inspect(engine)
    tables = set(inspector.get_table_names())

    app_tables = {"user", "dataset", "chatmessage"}
    existing_app_tables = tables.intersection(app_tables)

    if "alembic_version" not in tables and existing_app_tables:
        if not {"user", "dataset"}.issubset(tables):
            raise RuntimeError(
                "Partial legacy database detected. "
                "Automatic migration adoption has been stopped."
            )

        print("Existing legacy database detected.")
        print("Validating and reconciling schema...")

        reconcile_legacy_schema()

        print("Schema reconciliation successful.")
        print("Stamping initial migration...")

        command.stamp(config, "0001_initial")

    print("Applying pending Alembic migrations...")

    command.upgrade(config, "head")

    print("Migration completed successfully.")


if __name__ == "__main__":
    main()