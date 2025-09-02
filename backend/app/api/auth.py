from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.schemas.userschema import UserCreateSchema, UserReadSchema
from app.models.user import User
from app.security import hash_password
from app.deps import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserReadSchema, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreateSchema, db: Session = Depends(get_db)):
    # Check if email already exists
    existing = db.execute(select(User).where(User.email == payload.email)).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered.")

    # Hash password
    pw_hash = hash_password(payload.password)

    # Create and save user
    user = User(email=payload.email, password_hash=pw_hash)
    db.add(user)
    db.commit()
    db.refresh(user)

    # Return without password_hash (controlled by response_model)
    return user
