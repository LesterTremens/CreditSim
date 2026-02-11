from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import httpx
from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests as google_requests

from app.core.config import settings
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import GoogleAuthRequest, RefreshRequest, Token, UserRead
from app.services.auth import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    decode_access_token,
    decode_refresh_token,
    get_user_by_email,
    generate_oauth_placeholder_hash,
)

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> User:
    token_data = decode_access_token(token)
    if token_data.email is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = get_user_by_email(db, token_data.email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    access_token = create_access_token(user.email)
    refresh_token = create_refresh_token(user.email)
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


@router.post("/refresh", response_model=Token)
def refresh_access_token(payload: RefreshRequest) -> Token:
    token_data = decode_refresh_token(payload.refresh_token)
    if token_data.email is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    access_token = create_access_token(token_data.email)
    refresh_token = create_refresh_token(token_data.email)
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


@router.post("/google", response_model=Token)
def login_with_google(payload: GoogleAuthRequest, db: Session = Depends(get_db)) -> Token:
    if not settings.google_client_id or not settings.google_client_secret or not settings.google_redirect_uri:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Google OAuth not configured",
        )

    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": payload.code,
        "client_id": settings.google_client_id,
        "client_secret": settings.google_client_secret,
        "redirect_uri": settings.google_redirect_uri,
        "grant_type": "authorization_code",
    }
    if payload.code_verifier:
        data["code_verifier"] = payload.code_verifier

    try:
        response = httpx.post(token_url, data=data, timeout=10.0)
    except httpx.HTTPError:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Google token exchange failed")

    if response.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Google auth code")

    token_response = response.json()
    raw_id_token = token_response.get("id_token")
    if not raw_id_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing id_token from Google")

    try:
        idinfo = google_id_token.verify_oauth2_token(
            raw_id_token,
            google_requests.Request(),
            settings.google_client_id,
        )
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid id_token")

    email = idinfo.get("email")
    email_verified = bool(idinfo.get("email_verified"))
    provider_id = idinfo.get("sub")

    if not email or not provider_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid id_token payload")

    if settings.allowed_email_domains:
        allowed = {d.strip().lower() for d in settings.allowed_email_domains.split(",") if d.strip()}
        domain = email.split("@")[-1].lower()
        if allowed and domain not in allowed:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email domain not allowed")

    user = get_user_by_email(db, email)
    if not user:
        user = User(
            email=email,
            hashed_password=generate_oauth_placeholder_hash(),
            is_active=True,
            is_superuser=False,
            provider="google",
            provider_id=provider_id,
            email_verified=email_verified,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        updated = False
        if user.provider != "google":
            user.provider = "google"
            updated = True
        if user.provider_id != provider_id:
            user.provider_id = provider_id
            updated = True
        if email_verified and not user.email_verified:
            user.email_verified = True
            updated = True
        if updated:
            db.add(user)
            db.commit()
            db.refresh(user)

    access_token = create_access_token(user.email)
    refresh_token = create_refresh_token(user.email)
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


@router.get("/users/me", response_model=UserRead)
def read_users_me(current_user: User = Depends(get_current_user)) -> UserRead:
    return UserRead(
        id=str(current_user.id),
        email=current_user.email,
        is_active=current_user.is_active,
        is_superuser=current_user.is_superuser,
        email_verified=current_user.email_verified,
        provider=current_user.provider,
    )
