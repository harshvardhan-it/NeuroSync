from datetime import datetime, timedelta
from jose import jwt, JWTError
import bcrypt
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
)

def hash_password(password: str) -> str:
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(
        plain.encode("utf-8"),
        hashed.encode("utf-8")
    )

def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

def decode_token(token: str) -> dict:
    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlmodel import Session, select

from backend.utils.database import get_session
from backend.models.user import User

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


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
            select(User).where(
                User.email == email
            )
        ).first()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        return user

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )