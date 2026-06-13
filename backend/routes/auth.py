from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError

from sqlmodel import Session, select

from backend.models.user import User
from backend.schemas.auth_schema import RegisterSchema, LoginSchema
from backend.utils.database import get_session
from backend.utils.auth import (
    hash_password,
    verify_password,
    create_access_token,
    decode_token
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


@router.post("/register")
def register(
    data: RegisterSchema,
    session: Session = Depends(get_session)
):

    existing_user = session.exec(
        select(User).where(User.email == data.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    new_user = User(
        name=data.name,
        email=data.email,
        password=hash_password(data.password)
    )

    session.add(new_user)

    session.commit()

    session.refresh(new_user)

    token = create_access_token({
        "sub": data.email
    })

    return {
        "success": True,
        "message": "User registered successfully",
        "data": {
            "access_token": token
        }
    }


@router.post("/login")
def login(
    data: LoginSchema,
    session: Session = Depends(get_session)
):

    user = session.exec(
        select(User).where(User.email == data.email)
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not verify_password(
        data.password,
        user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_access_token({
        "sub": user.email
    })

    return {
        "success": True,
        "message": "Login successful",
        "data": {
            "access_token": token
        }
    }


@router.get("/me")
def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
):

    try:

        payload = decode_token(token)

        email = payload.get("sub")

        if not email:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        user = session.exec(
            select(User).where(User.email == email)
        ).first()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        return {
            "success": True,
            "message": "User retrieved successfully",
            "data": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "focus_score": user.focus_score,
                "streak": user.streak
            }
        }

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )