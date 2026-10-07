from pathlib import Path
from uuid import uuid4
from datetime import datetime, timezone

import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from backend.ai.analyzer import analyze_dataframe
from backend.models.dataset import Dataset
from backend.models.user import User
from backend.services.executive_summary_service import ExecutiveSummaryService
from backend.services.pdf_report_service import PDFReportService
from backend.services.report_service import ReportService
from backend.utils.auth import get_current_user
from backend.utils.database import get_session
from backend.utils.logger import logger


router = APIRouter(prefix="/dataset", tags=["Dataset"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
MAX_FILE_SIZE = 10 * 1024 * 1024


def _read_dataset(file_path: Path, extension: str):
    if extension == "csv":
        return pd.read_csv(file_path)
    return pd.read_excel(file_path, engine="openpyxl")


def _cleanup(path: Path | None):
    if path and path.exists():
        try:
            path.unlink()
        except OSError:
            logger.exception("Failed to remove temporary upload %s", path)


def _get_owned_dataset(dataset_id: int, current_user: User, session: Session):
    dataset = session.get(Dataset, dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found.")
    if dataset.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied.")
    return dataset


@router.post("/upload")
def upload_dataset(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    original_name = Path(file.filename or "").name
    extension = Path(original_name).suffix.lower().lstrip(".")

    if extension not in {"csv", "xlsx"}:
        raise HTTPException(status_code=400, detail="Only CSV and XLSX files are supported.")

    contents = file.file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds the 10 MB limit.")
    file.file.seek(0)

    storage_name = f"{uuid4().hex}.{extension}"
    file_path = UPLOAD_DIR / storage_name

    try:
        file_path.write_bytes(contents)

        try:
            df = _read_dataset(file_path, extension)
        except Exception:
            logger.exception("Dataset parsing failed for user=%s", current_user.id)
            raise HTTPException(status_code=400, detail="Invalid or corrupted dataset file.")

        if df.empty:
            raise HTTPException(status_code=400, detail="Dataset is empty.")
        if len(df.columns) == 0:
            raise HTTPException(status_code=400, detail="Dataset contains no columns.")
        if len(df.columns) > 50000:
            raise HTTPException(status_code=400, detail="Dataset contains too many columns.")

        try:
            analysis = analyze_dataframe(df)
        except Exception:
            logger.exception("Dataset analysis failed for user=%s", current_user.id)
            raise HTTPException(status_code=500, detail="Dataset analysis failed. Please try again.")

        dataset = Dataset(
            user_id=current_user.id,
            filename=storage_name,
            file_type=extension,
            rows=len(df),
            columns=len(df.columns),
            status="analyzed",
            analysis_result=analysis,
        )

        try:
            session.add(dataset)
            session.commit()
            session.refresh(dataset)
        except IntegrityError:
            session.rollback()
            logger.exception("Dataset persistence failed for user=%s", current_user.id)
            raise HTTPException(status_code=500, detail="Dataset could not be saved.")

        logger.info(
            "Dataset analyzed: user=%s dataset=%s rows=%s columns=%s",
            current_user.id, dataset.id, dataset.rows, dataset.columns
        )

        return {
            "success": True,
            "message": "Dataset uploaded and analyzed successfully.",
            "data": {
                "dataset_id": dataset.id,
                "filename": original_name,
                "rows": dataset.rows,
                "columns": dataset.columns,
                "uploaded_at": datetime.now(timezone.utc).isoformat(),
                "analysis": analysis,
            },
        }

    except HTTPException:
        session.rollback()
        _cleanup(file_path)
        raise
    except Exception:
        session.rollback()
        _cleanup(file_path)
        logger.exception("Unexpected dataset upload failure for user=%s", current_user.id)
        raise HTTPException(status_code=500, detail="Dataset upload failed. Please try again.")


@router.get("/")
def get_user_datasets(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    datasets = session.exec(
        select(Dataset)
        .where(Dataset.user_id == current_user.id)
        .order_by(Dataset.id.desc())
    ).all()

    return {
        "success": True,
        "message": "Datasets fetched successfully.",
        "data": [
            {
                "id": d.id,
                "filename": d.filename,
                "rows": d.rows,
                "columns": d.columns,
                "status": d.status,
                "uploaded_at": d.uploaded_at.isoformat(),
            }
            for d in datasets
        ],
    }


@router.get("/{dataset_id}")
def get_dataset(
    dataset_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    dataset = _get_owned_dataset(dataset_id, current_user, session)
    return {
        "success": True,
        "message": "Dataset retrieved successfully.",
        "data": {
            "dataset_id": dataset.id,
            "filename": dataset.filename,
            "analysis": dataset.analysis_result,
        },
    }


@router.get("/{dataset_id}/executive-summary")
def get_executive_summary(
    dataset_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    dataset = _get_owned_dataset(dataset_id, current_user, session)
    return {
        "success": True,
        "message": "Executive summary generated.",
        "data": ExecutiveSummaryService.generate(dataset.analysis_result or {}),
    }


def _report(dataset, kind):
    analysis = dataset.analysis_result or {}
    if kind == "executive":
        return ReportService.generate_executive_report(analysis)
    if kind == "risk":
        return ReportService.generate_risk_report(analysis)
    if kind == "growth":
        return ReportService.generate_growth_report(analysis)
    return ReportService.generate_board_report(analysis)


@router.get("/{dataset_id}/reports/executive")
def executive_report(dataset_id: int, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    return {"success": True, "message": "Executive report generated.", "data": _report(_get_owned_dataset(dataset_id, current_user, session), "executive")}


@router.get("/{dataset_id}/reports/risk")
def risk_report(dataset_id: int, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    return {"success": True, "message": "Risk report generated.", "data": _report(_get_owned_dataset(dataset_id, current_user, session), "risk")}


@router.get("/{dataset_id}/reports/growth")
def growth_report(dataset_id: int, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    return {"success": True, "message": "Growth report generated.", "data": _report(_get_owned_dataset(dataset_id, current_user, session), "growth")}


@router.get("/{dataset_id}/reports/board")
def board_report(dataset_id: int, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    return {"success": True, "message": "Board report generated.", "data": _report(_get_owned_dataset(dataset_id, current_user, session), "board")}


@router.get("/{dataset_id}/reports/executive/pdf")
def executive_pdf(
    dataset_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    dataset = _get_owned_dataset(dataset_id, current_user, session)
    report = ReportService.generate_executive_report(dataset.analysis_result or {})
    try:
        pdf_path = PDFReportService.generate_executive_pdf(report, dataset_id)
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=f"executive_report_{dataset_id}.pdf",
        )
    except Exception:
        logger.exception("PDF generation failed for dataset=%s", dataset_id)
        raise HTTPException(status_code=500, detail="Report generation failed. Please try again.")
