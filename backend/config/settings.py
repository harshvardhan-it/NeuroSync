import os
from dotenv import load_dotenv

load_dotenv("backend/.env")


class Settings:

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///neurosync.db"
    )

    DEBUG = os.getenv(
        "DEBUG",
        "False"
    ).lower() == "true"

    SECRET_KEY = os.getenv("SECRET_KEY")

    ALGORITHM = os.getenv("ALGORITHM")

    ACCESS_TOKEN_EXPIRE_MINUTES = int(
        os.getenv(
            "ACCESS_TOKEN_EXPIRE_MINUTES",
            "60"
        )
    )


settings = Settings()