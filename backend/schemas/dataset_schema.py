from pydantic import BaseModel
from datetime import datetime


class DatasetResponse(BaseModel):
    id: int
    filename: str
    file_type: str
    rows: int
    columns: int
    status: str
    uploaded_at: datetime


class DatasetUploadResponse(BaseModel):
    message: str
    dataset_id: int