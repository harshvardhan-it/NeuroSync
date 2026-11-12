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

def _build_history(session: Session, user_id: int, dataset_id: int) -> list:
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
        return []
    
    # Return as a list of dicts in chronological order (oldest first)
    return [{"role": msg.role, "content": msg.content} for msg in reversed(rows)]

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

    # Pass the whole analysis object. The groq_service will handle truncating large arrays.
    analysis_context = dataset.analysis_result or {} 

    # This is now a list of message dictionaries, not a string
    history = _build_history(session, current_user.id, data.dataset_id)

    response = ask_ai(
        message=data.message,
        analysis=analysis_context,
        conversation_history=history,
    )

    # Save to DB
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

@router.get("/history/{dataset_id}")
def chat_history(
    dataset_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    dataset = session.get(Dataset, dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found.")
    if dataset.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied.")

    messages = session.exec(
        select(ChatMessage)
        .where(
            ChatMessage.user_id == current_user.id,
            ChatMessage.dataset_id == dataset_id,
        )
        .order_by(ChatMessage.created_at.desc())
        .limit(50)
    ).all()

    return {
        "success": True,
        "data": [
            {"role": message.role, "content": message.content}
            for message in reversed(messages)
        ],
    }

@router.delete("/history/{dataset_id}")
def clear_chat_history(
    dataset_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    dataset = session.get(Dataset, dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found.")
    if dataset.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied.")

    messages = session.exec(
        select(ChatMessage).where(
            ChatMessage.user_id == current_user.id,
            ChatMessage.dataset_id == dataset_id,
        )
    ).all()

    for message in messages:
        session.delete(message)
    session.commit()

    return {"success": True, "message": "Chat history cleared.", "data": None}
    