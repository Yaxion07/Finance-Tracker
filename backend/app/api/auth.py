from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User
from app.schemas.userschema import UserLoginSchema, TokenSchema, UserReadSchema, UserCreateSchema
from app.security import verify_password, create_access_token, hash_password, ACCESS_TOKEN_EXPIRE_MINUTES
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

@router.post("/login", response_model=TokenSchema)
def login(payload: UserLoginSchema, db: Session = Depends(get_db)):
    user = db.execute(select(User).where(User.email == payload.email)).scalar_one_or_none()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=401, 
            detail="Could not find user, invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
            )
    # If user is found and password is correct, create and return JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
    data={"sub": str(user.id)},
    expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# No-op endpoint. Client has to invalidate token manually through frontend.
@router.delete("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout():
    return {"message": "Logged out successfully"}
    
    