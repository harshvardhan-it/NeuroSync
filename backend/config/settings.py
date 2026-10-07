from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    """Typed, validated application configuration."""

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    APP_ENV: str = "development"
    DEBUG: bool = False

    DATABASE_URL: str = "sqlite:///./neurosync.db"
    GROQ_API_KEY: str | None = None

    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    ALLOWED_ORIGINS: list[str] = ["http://localhost:5173"]

    MAX_UPLOAD_SIZE_MB: int = 10
    MAX_DATASET_ROWS: int = 250_000
    MAX_DATASET_COLUMNS: int = 200
    MAX_DATASET_CELLS: int = 5_000_000
    AI_MAX_MESSAGE_LENGTH: int = 4000

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_origins(cls, value):
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    def validate_runtime(self) -> None:
        if self.APP_ENV.lower() == "production":
            if not self.SECRET_KEY or self.SECRET_KEY == "CHANGE_ME_IN_PRODUCTION":
                raise RuntimeError("SECRET_KEY must be configured in production.")
            if self.DATABASE_URL.startswith("sqlite"):
                raise RuntimeError("A PostgreSQL DATABASE_URL is required in production.")
            if not self.ALLOWED_ORIGINS:
                raise RuntimeError("ALLOWED_ORIGINS must contain at least one origin.")


settings = Settings()
settings.validate_runtime()
