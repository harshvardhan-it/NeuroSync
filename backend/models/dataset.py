from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import Column, JSON, Index
from sqlmodel import Field, SQLModel


class Dataset(SQLModel, table=True):
    __table_args__ = (
        Index("ix_dataset_user_id", "user_id"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
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
