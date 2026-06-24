from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlmodel import Session

from backend.services.executive_summary_service import (
    ExecutiveSummaryService
)
from backend.services.report_service import (
    ReportService
)
from backend.models.dataset import Dataset
from backend.models.user import User

from backend.utils.database import get_session
from backend.utils.auth import get_current_user
from backend.utils.logger import logger

from backend.ai.analyzer import analyze_dataframe
from datetime import datetime

import pandas as pd
import os
import shutil

router = APIRouter(
    prefix="/dataset",
    tags=["Dataset"]
)

UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


@router.post("/upload")
def upload_dataset(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):

    logger.info(
        f"Dataset upload started by user {current_user.id}"
    )

    # -----------------------------
    # File Type Validation
    # -----------------------------

    file_extension = file.filename.split(".")[-1].lower()

    if file_extension not in ["csv", "xlsx"]:
        raise HTTPException(
            status_code=400,
            detail="Only CSV and XLSX files are supported"
        )

    # -----------------------------
    # File Size Validation
    # -----------------------------

    contents = file.file.read()

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds 10MB limit"
        )

    file.file.seek(0)

    # -----------------------------
    # Unique Filename Generation
    # -----------------------------

    timestamp = datetime.utcnow().strftime(
        "%Y%m%d_%H%M%S"
    )

    safe_filename = (
        f"{timestamp}_{file.filename}"
    )

    file_path = os.path.join(
        UPLOAD_DIR,
        safe_filename
    )

    # -----------------------------
    # Save File
    # -----------------------------

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    # -----------------------------
    # Read Dataset Safely
    # -----------------------------

    try:

        if file_extension == "csv":
            df = pd.read_csv(file_path)

        else:
            df = pd.read_excel(file_path)

    except Exception:

        logger.exception(
            f"Failed to read file {file.filename}"
        )

        raise HTTPException(
            status_code=400,
            detail="Invalid or corrupted file"
        )

    # -----------------------------
    # Dataset Validation
    # -----------------------------

    if df.empty:
        raise HTTPException(
            status_code=400,
            detail="Dataset is empty"
        )

    if len(df.columns) == 0:
        raise HTTPException(
            status_code=400,
            detail="Dataset contains no columns"
        )

    # -----------------------------
    # Analysis Protection
    # -----------------------------

    try:

        analysis = analyze_dataframe(df)

    except Exception:

        logger.exception(
            f"Analysis failed for file {file.filename}"
        )

        raise HTTPException(
            status_code=500,
            detail="Dataset analysis failed"
        )

    # -----------------------------
    # Store Dataset
    # -----------------------------

    dataset = Dataset(
        user_id=current_user.id,
        filename=safe_filename,
        file_type=file_extension,
        rows=len(df),
        columns=len(df.columns),
        status="uploaded",
        analysis_result=analysis
    )

    session.add(dataset)
    session.commit()
    session.refresh(dataset)

    logger.info(
        f"Dataset {dataset.id} uploaded successfully"
    )

    return {
        "success": True,
        "message": "Dataset uploaded successfully",
        "data": {
            "dataset_id": dataset.id,
            "filename": file.filename,
            "rows": dataset.rows,
            "columns": dataset.columns,
            "uploaded_at": datetime.utcnow().isoformat(),
            "analysis": analysis
        }
    }


@router.get("/{dataset_id}/executive-summary")
def get_executive_summary(
    dataset_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):

    dataset = session.get(
        Dataset,
        dataset_id
    )

    if not dataset:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    if dataset.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    logger.info(
        f"Executive summary requested for dataset {dataset_id}"
    )

    summary = ExecutiveSummaryService.generate(
        dataset.analysis_result
    )

    return {
        "success": True,
        "message": "Executive summary generated",
        "data": summary
    }

@router.get("/{dataset_id}")
def get_dataset(
    dataset_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):

    dataset = session.get(
        Dataset,
        dataset_id
    )

    if not dataset:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    if dataset.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    logger.info(
        f"Dataset {dataset_id} accessed by user {current_user.id}"
    )

    return {
        "success": True,
        "message": "Dataset retrieved successfully",
        "data": {
            "dataset_id": dataset.id,
            "filename": dataset.filename,
            "analysis": dataset.analysis_result
        }
    }

@router.get("/")
def get_user_datasets(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    datasets = session.query(Dataset).filter(
        Dataset.user_id == current_user.id
    ).order_by(
        Dataset.id.desc()
    ).all()

    return {
        "success": True,
        "message": "Datasets fetched successfully",
        "data": [
            {
                "id": d.id,
                "filename": d.filename,
                "rows": d.rows,
                "columns": d.columns,
                "status": d.status,
            }
            for d in datasets
        ]
    }

@router.get("/{dataset_id}/reports/executive")
def get_executive_report(
    dataset_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):

    dataset = session.get(
        Dataset,
        dataset_id
    )

    if not dataset:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    if dataset.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    report = (
        ReportService.generate_executive_report(
            dataset.analysis_result
        )
    )

    return {
        "success": True,
        "data": report
    }

@router.get("/{dataset_id}/reports/risk")
def get_risk_report(
    dataset_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):

    dataset = session.get(
        Dataset,
        dataset_id
    )

    if not dataset:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    if dataset.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    report = (
        ReportService.generate_risk_report(
            dataset.analysis_result
        )
    )

    return {
        "success": True,
        "data": report
    }

@router.get("/{dataset_id}/reports/growth")
def get_growth_report(
    dataset_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):

    dataset = session.get(
        Dataset,
        dataset_id
    )

    if not dataset:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    if dataset.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    report = (
        ReportService.generate_growth_report(
            dataset.analysis_result
        )
    )

    return {
        "success": True,
        "data": report
    }

@router.get("/{dataset_id}/reports/board")
def get_board_report(
    dataset_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):

    dataset = session.get(
        Dataset,
        dataset_id
    )

    if not dataset:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    if dataset.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    report = (
        ReportService.generate_board_report(
            dataset.analysis_result
        )
    )

    return {
        "success": True,
        "data": report
    }
