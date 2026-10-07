from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlmodel import Session

from backend.ai.conversation_context import conversation_manager
from backend.ai.groq_service import ask_ai
from backend.models.dataset import Dataset
from backend.models.user import User
from backend.utils.auth import get_current_user
from backend.utils.database import get_session
from backend.utils.logger import logger


router = APIRouter(prefix="/ai", tags=["AI"])


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    dataset_id: int


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
        logger.warning(
            "Unauthorized AI dataset access: user=%s dataset=%s",
            current_user.id,
            data.dataset_id,
        )
        raise HTTPException(status_code=403, detail="Access denied.")

    analysis = dataset.analysis_result or {}

    history = conversation_manager.build_context(
        user_id=current_user.id,
        dataset_id=data.dataset_id,
    )

    response = ask_ai(
        message=data.message,
        analysis=analysis,
        conversation_history=history,
    )

    conversation_manager.add_message(
        user_id=current_user.id,
        dataset_id=data.dataset_id,
        role="user",
        content=data.message,
    )
    conversation_manager.add_message(
        user_id=current_user.id,
        dataset_id=data.dataset_id,
        role="assistant",
        content=response,
    )

    return {
        "success": True,
        "message": "Executive AI response generated.",
        "data": response,
    }
