from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlmodel import Session

from backend.ai.groq_service import ask_ai
from backend.ai.conversation_context import conversation_manager
from backend.config.settings import settings
from backend.models.dataset import Dataset
from backend.models.user import User
from backend.utils.auth import get_current_user
from backend.utils.database import get_session

router = APIRouter(prefix="/ai", tags=["AI"])


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=settings.AI_MAX_MESSAGE_LENGTH)
    dataset_id: int = Field(gt=0)


@router.post("/chat")
def chat(
    data: ChatRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    dataset = session.get(Dataset, data.dataset_id)

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found.")

    if dataset.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied.")

    analysis = dataset.analysis_result or {}

    analysis_context = {
        key: analysis.get(key)
        for key in (
            "business_status",
            "health_score",
            "business_understanding",
            "executive_summary",
            "dataset_summary",
            "kpis",
            "insights",
            "anomalies",
            "risk_assessment",
            "forecasts",
            "recommendations",
            "decisions",
            "executive_action_plan",
            "root_cause_analysis",
            "correlation_analysis",
            "dependency_analysis",
            "causal_analysis",
            "strategic_leverage_analysis",
            "executive_optimization",
            "scenario_simulations",
        )
    }

    history = conversation_manager.build_context(
        current_user.id,
        data.dataset_id,
    )

    response = ask_ai(
        message=data.message,
        analysis=analysis_context,
        conversation_history=history,
    )

    conversation_manager.add_message(
        current_user.id,
        data.dataset_id,
        "user",
        data.message,
    )
    conversation_manager.add_message(
        current_user.id,
        data.dataset_id,
        "assistant",
        response,
    )

    return {
        "success": True,
        "message": "AI response generated.",
        "data": response,
    }
