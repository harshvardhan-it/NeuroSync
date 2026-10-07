from typing import Optional

from sqlalchemy import Column, String, UniqueConstraint
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint("email", name="uq_user_email"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(
        sa_column=Column(String(320), nullable=False, unique=True, index=True)
    )
    password: str

    focus_score: int = 0
    streak: int = 0
