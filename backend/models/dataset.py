from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel


class Dataset(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(index=True)

    # Stored object key, never the raw client filename.
    filename: str
    file_type: str

    rows: int = 0
    columns: int = 0

    status: str = "uploaded"

    analysis_result: Optional[dict] = Field(
        default=None,
        sa_column=Column(JSON),
    )

    uploaded_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
