import os

from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

load_dotenv(
    BASE_DIR / ".env"
)


class Settings:

    GROQ_API_KEY = os.getenv(
        "GROQ_API_KEY"
    )

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///neurosync.db"
    )

    DEBUG = os.getenv(
        "DEBUG",
        "False"
    ).lower() == "true"

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "CHANGE_ME_IN_PRODUCTION"
    )

    ALGORITHM = os.getenv(
        "ALGORITHM",
        "HS256"
    )

    ACCESS_TOKEN_EXPIRE_MINUTES = int(
        os.getenv(
            "ACCESS_TOKEN_EXPIRE_MINUTES",
            "60"
        )
    )

    ALLOWED_ORIGINS = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:5173"
    ).split(",")

    @classmethod
    def validate(cls):

        if cls.SECRET_KEY == "CHANGE_ME_IN_PRODUCTION":

            print(
                "WARNING: Using default SECRET_KEY."
            )


settings = Settings()

settings.validate()