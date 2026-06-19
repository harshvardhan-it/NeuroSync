from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session

from backend.ai.groq_service import ask_ai
from backend.models.dataset import Dataset

from backend.utils.database import get_session

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


class ChatRequest(BaseModel):
    message: str
    dataset_id: int


@router.post("/chat")
def chat(
    data: ChatRequest,
    session: Session = Depends(get_session)
):
    dataset = session.get(
        Dataset,
        data.dataset_id
    )

    if not dataset:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    analysis = dataset.analysis_result or {}

    # Build a clean AI context instead of
    # sending the entire raw analysis object
    analysis_context = {
        "executive_summary":
            analysis.get(
                "executive_summary"
            ),

        "dataset_summary":
            analysis.get(
                "dataset_summary"
            ),

        "kpis":
            analysis.get(
                "kpis"
            ),

        "insights":
            analysis.get(
                "insights"
            ),

        "anomalies":
            analysis.get(
                "anomalies"
            ),

        "risk_assessment":
            analysis.get(
                "risk_assessment"
            ),

        "forecasts":
            analysis.get(
                "forecasts"
            ),

        "recommendations":
            analysis.get(
                "recommendations"
            ),

        "decisions":
            analysis.get(
                "decisions"
            ),

        "executive_action_plan":
            analysis.get(
                "executive_action_plan"
            )
    }

    response = ask_ai(
        message=data.message,
        analysis=analysis_context
    )

    return {
        "success": True,
        "data": response
    }