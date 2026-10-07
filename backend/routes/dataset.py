from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlmodel import Session, select

from backend.ai.analyzer import analyze_dataframe
from backend.config.settings import settings
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

MAX_FILE_SIZE = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
ALLOWED_EXTENSIONS = {"csv", "xlsx"}


def _get_owned_dataset(dataset_id: int, user: User, session: Session) -> Dataset:
    dataset = session.get(Dataset, dataset_id)

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found.")

    if dataset.user_id != user.id:
        raise HTTPException(status_code=403, detail="Access denied.")

    return dataset


def _safe_storage_name(extension: str) -> str:
    return f"{uuid4().hex}.{extension}"


@router.post("/upload")
def upload_dataset(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    original_name = Path(file.filename or "dataset").name
    extension = Path(original_name).suffix.lower().lstrip(".")

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only CSV and XLSX files are supported.",
        )

    contents = file.file.read(MAX_FILE_SIZE + 1)
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File size must be {settings.MAX_UPLOAD_SIZE_MB} MB or smaller.",
        )

    storage_name = _safe_storage_name(extension)
    file_path = UPLOAD_DIR / storage_name

    try:
        file_path.write_bytes(contents)

        if extension == "csv":
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)

        if df.empty:
            raise HTTPException(status_code=400, detail="Dataset is empty.")

        if len(df.columns) == 0:
            raise HTTPException(status_code=400, detail="Dataset contains no columns.")

        if len(df) > settings.MAX_DATASET_ROWS:
            raise HTTPException(
                status_code=413,
                detail=f"Dataset exceeds the {settings.MAX_DATASET_ROWS:,} row limit.",
            )

        if len(df.columns) > settings.MAX_DATASET_COLUMNS:
            raise HTTPException(
                status_code=413,
                detail=f"Dataset exceeds the {settings.MAX_DATASET_COLUMNS} column limit.",
            )

        if len(df) * len(df.columns) > settings.MAX_DATASET_CELLS:
            raise HTTPException(
                status_code=413,
                detail="Dataset is too large to process safely.",
            )

        status = "processing"
        dataset = Dataset(
            user_id=current_user.id,
            filename=storage_name,
            file_type=extension,
            rows=len(df),
            columns=len(df.columns),
            status=status,
        )
        session.add(dataset)
        session.commit()
        session.refresh(dataset)

        try:
            analysis = analyze_dataframe(df)
            dataset.analysis_result = analysis
            dataset.status = "completed"
            session.add(dataset)
            session.commit()
            session.refresh(dataset)
        except Exception:
            dataset.status = "failed"
            session.add(dataset)
            session.commit()
            logger.exception("Analysis failed for dataset %s", dataset.id)
            raise HTTPException(
                status_code=500,
                detail="Dataset analysis failed. Please try another dataset.",
            )

        logger.info(
            "Dataset %s uploaded successfully by user %s",
            dataset.id,
            current_user.id,
        )

        return {
            "success": True,
            "message": "Dataset uploaded and analyzed successfully.",
            "data": {
                "dataset_id": dataset.id,
                "filename": original_name,
                "rows": dataset.rows,
                "columns": dataset.columns,
                "status": dataset.status,
                "uploaded_at": datetime.now(timezone.utc).isoformat(),
                "analysis": analysis,
            },
        }

    except HTTPException:
        if file_path.exists():
            file_path.unlink(missing_ok=True)
        raise
    except Exception:
        if file_path.exists():
            file_path.unlink(missing_ok=True)
        logger.exception("Dataset upload failed for user %s", current_user.id)
        raise HTTPException(
            status_code=400,
            detail="Invalid or corrupted dataset.",
        )


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
            "status": dataset.status,
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

    summary = ExecutiveSummaryService.generate(dataset.analysis_result or {})

    return {
        "success": True,
        "message": "Executive summary generated.",
        "data": summary,
    }


def _report(dataset: Dataset, report_type: str):
    generators = {
        "executive": ReportService.generate_executive_report,
        "risk": ReportService.generate_risk_report,
        "growth": ReportService.generate_growth_report,
        "board": ReportService.generate_board_report,
    }
    return generators[report_type](dataset.analysis_result or {})


@router.get("/{dataset_id}/reports/{report_type}")
def get_report(
    dataset_id: int,
    report_type: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    if report_type not in {"executive", "risk", "growth", "board"}:
        raise HTTPException(status_code=404, detail="Report type not found.")

    dataset = _get_owned_dataset(dataset_id, current_user, session)

    return {
        "success": True,
        "data": _report(dataset, report_type),
    }


@router.get("/{dataset_id}/reports/executive/pdf")
def download_executive_pdf(
    dataset_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    dataset = _get_owned_dataset(dataset_id, current_user, session)

    report = _report(dataset, "executive")
    pdf_path = PDFReportService.generate_executive_pdf(report, dataset_id)

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=f"executive_report_{dataset_id}.pdf",
    )
