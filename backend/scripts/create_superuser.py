import argparse
import getpass
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if BACKEND_ROOT not in sys.path:
    sys.path.insert(0, BACKEND_ROOT)

from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.user import User
from app.services.auth import get_password_hash


def _get_or_create_superuser(db: Session, email: str, password: str) -> User:
    user = db.query(User).filter(User.email == email).first()
    if user:
        user.hashed_password = get_password_hash(password)
        user.is_superuser = True
        user.is_active = True
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    user = User(
        email=email,
        hashed_password=get_password_hash(password),
        is_superuser=True,
        is_active=True,
        email_verified=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def main() -> None:
    parser = argparse.ArgumentParser(description="Create or promote a superuser.")
    parser.add_argument("--email", required=True, help="Email for the superuser")
    parser.add_argument(
        "--password",
        help="Password for the superuser (omit to be prompted)",
    )
    args = parser.parse_args()

    password = args.password or getpass.getpass("Password: ")

    db = SessionLocal()
    try:
        user = _get_or_create_superuser(db, args.email, password)
        print(f"Superuser ready: {user.email}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
