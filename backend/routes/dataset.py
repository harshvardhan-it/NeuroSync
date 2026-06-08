from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlmodel import Session

from models.dataset import Dataset
from utils.database import get_session

from ai.analyzer import analyze_dataframe

import pandas as pd
import os
import shutil

router = APIRouter(
    prefix="/dataset",
    tags=["Dataset"]
)

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
def upload_dataset(
    file: UploadFile = File(...),
    session: Session = Depends(get_session)
):

    file_extension = file.filename.split(".")[-1].lower()

    if file_extension not in ["csv", "xlsx"]:
        raise HTTPException(
            status_code=400,
            detail="Only CSV and XLSX files are supported"
        )

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    if file_extension == "csv":
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    analysis = analyze_dataframe(df)

    dataset = Dataset(
        user_id=1,  # temporary
        filename=file.filename,
        file_type=file_extension,
        rows=len(df),
        columns=len(df.columns),
        status="uploaded"
    )

    session.add(dataset)
    session.commit()
    session.refresh(dataset)

    return {
        "message": "Dataset uploaded successfully",
        "dataset_id": dataset.id,
        "analysis": analysis
    }