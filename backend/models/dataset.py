from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class Dataset(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int

    filename: str
    file_type: str

    rows: int = 0
    columns: int = 0

    status: str = "uploaded"

    uploaded_at: datetime = Field(default_factory=datetime.utcnow)