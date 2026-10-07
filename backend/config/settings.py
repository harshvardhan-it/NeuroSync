import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


class Settings:
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development").strip().lower()
    DEBUG = os.getenv("DEBUG", "false").strip().lower() == "true"

    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip() or None
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///neurosync.db").strip()

    SECRET_KEY = os.getenv("SECRET_KEY", "").strip()
    DEFAULT_SECRET_KEY = "CHANGE_ME_IN_PRODUCTION"

    ALGORITHM = os.getenv("ALGORITHM", "HS256").strip()
    ACCESS_TOKEN_EXPIRE_MINUTES = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
    )

    ALLOWED_ORIGINS = [
        origin.strip()
        for origin in os.getenv(
            "ALLOWED_ORIGINS",
            "http://localhost:5173"
        ).split(",")
        if origin.strip()
    ]

    def validate(self):
        if self.ACCESS_TOKEN_EXPIRE_MINUTES <= 0:
            raise RuntimeError("ACCESS_TOKEN_EXPIRE_MINUTES must be greater than 0.")

        if self.ENVIRONMENT == "production":
            if not self.SECRET_KEY:
                raise RuntimeError(
                    "SECRET_KEY is required when ENVIRONMENT=production."
                )
            if self.SECRET_KEY == self.DEFAULT_SECRET_KEY:
                raise RuntimeError(
                    "SECRET_KEY uses the insecure development default."
                )
            if len(self.SECRET_KEY) < 32:
                raise RuntimeError(
                    "SECRET_KEY must be at least 32 characters in production."
                )
            if "*" in self.ALLOWED_ORIGINS:
                raise RuntimeError(
                    "Wildcard CORS origin is not allowed in production."
                )
        elif not self.SECRET_KEY:
            # Development-only fallback. Never silently allowed in production.
            self.SECRET_KEY = self.DEFAULT_SECRET_KEY


settings = Settings()
settings.validate()
