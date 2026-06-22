from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session

from backend.ai.groq_service import ask_ai
from backend.ai.conversation_context import (
    conversation_manager
)

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

    analysis = (
        dataset.analysis_result
        or {}
    )

    analysis_context = {

        "business_status":
            analysis.get(
                "business_status"
            ),

        "health_score":
            analysis.get(
                "health_score"
            ),

        "business_understanding":
            analysis.get(
                "business_understanding"
            ),

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

    history = (
        conversation_manager
        .build_context(
            data.dataset_id
        )
    )

    response = ask_ai(
        message=data.message,
        analysis=analysis_context,
        conversation_history=history
    )

    conversation_manager.add_message(
        data.dataset_id,
        "user",
        data.message
    )

    conversation_manager.add_message(
        data.dataset_id,
        "assistant",
        response
    )

    return {
        "success": True,
        "data": response
    }