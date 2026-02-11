from datetime import datetime, timedelta, timezone
from typing import Optional
import secrets

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.user import User
from app.schemas.auth import TokenData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def create_refresh_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta is None:
        expires_delta = timedelta(days=settings.refresh_token_expire_days)
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"sub": subject, "exp": expire}
    secret = settings.refresh_secret_key or settings.secret_key
    return jwt.encode(to_encode, secret, algorithm=settings.algorithm)


def decode_access_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email: str | None = payload.get("sub")
        if email is None:
            return TokenData(email=None)
        return TokenData(email=email)
    except JWTError:
        return TokenData(email=None)


def decode_refresh_token(token: str) -> TokenData:
    try:
        secret = settings.refresh_secret_key or settings.secret_key
        payload = jwt.decode(token, secret, algorithms=[settings.algorithm])
        email: str | None = payload.get("sub")
        if email is None:
            return TokenData(email=None)
        return TokenData(email=email)
    except JWTError:
        return TokenData(email=None)


def generate_oauth_placeholder_hash() -> str:
    # Random hash so OAuth users cannot login with password
    return get_password_hash(secrets.token_urlsafe(32))
