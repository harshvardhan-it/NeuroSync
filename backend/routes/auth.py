from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from backend.models.user import User
from backend.schemas.auth_schema import LoginSchema, RegisterSchema
from backend.utils.auth import create_access_token, get_current_user, hash_password, verify_password
from backend.utils.database import get_session

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register(data: RegisterSchema, session: Session = Depends(get_session)):
    email = data.email.strip().lower()

    existing_user = session.exec(select(User).where(User.email == email)).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already exists.")

    new_user = User(
        name=data.name.strip(),
        email=email,
        password=hash_password(data.password),
    )

    session.add(new_user)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Email already exists.")

    session.refresh(new_user)

    return {
        "success": True,
        "message": "User registered successfully.",
        "data": {"access_token": create_access_token({"sub": new_user.email})},
    }


@router.post("/login")
def login(data: LoginSchema, session: Session = Depends(get_session)):
    email = data.email.strip().lower()
    user = session.exec(select(User).where(User.email == email)).first()

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials.")

    return {
        "success": True,
        "message": "Login successful.",
        "data": {"access_token": create_access_token({"sub": user.email})},
    }


@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return {
        "success": True,
        "message": "User retrieved successfully.",
        "data": {
            "id": current_user.id,
            "name": current_user.name,
            "email": current_user.email,
            "focus_score": current_user.focus_score,
            "streak": current_user.streak,
        },
    }
