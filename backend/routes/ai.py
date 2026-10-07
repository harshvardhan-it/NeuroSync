from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlmodel import Session, select

from backend.ai.groq_service import ask_ai
from backend.config.settings import settings
from backend.models.chat_message import ChatMessage
from backend.models.dataset import Dataset
from backend.models.user import User
from backend.utils.auth import get_current_user
from backend.utils.database import get_session

router = APIRouter(prefix="/ai", tags=["AI"])


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=settings.AI_MAX_MESSAGE_LENGTH)
    dataset_id: int = Field(gt=0)


def _build_history(session: Session, user_id: int, dataset_id: int) -> str:
    rows = session.exec(
        select(ChatMessage)
        .where(
            ChatMessage.user_id == user_id,
            ChatMessage.dataset_id == dataset_id,
        )
        .order_by(ChatMessage.created_at.desc())
        .limit(10)
    ).all()

    if not rows:
        return ""

    lines = ["\nPREVIOUS DISCUSSION\n"]
    for message in reversed(rows):
        role = "User" if message.role == "user" else "AI"
        lines.append(f"{role}: {message.content}\n")
    return "\n".join(lines)


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

    history = _build_history(
        session,
        current_user.id,
        data.dataset_id,
    )

    response = ask_ai(
        message=data.message,
        analysis=analysis_context,
        conversation_history=history,
    )

    session.add_all([
        ChatMessage(
            user_id=current_user.id,
            dataset_id=data.dataset_id,
            role="user",
            content=data.message,
        ),
        ChatMessage(
            user_id=current_user.id,
            dataset_id=data.dataset_id,
            role="assistant",
            content=response,
        ),
    ])
    session.commit()

    return {
        "success": True,
        "message": "AI response generated.",
        "data": response,
    }
