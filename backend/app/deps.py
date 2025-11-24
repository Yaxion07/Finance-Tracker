from jose import JWTError
from app.database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer

from app.security import SECRET_KEY, ALGORITHM
from app.models.user import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Returns a DB session that closes automatically. Used when handling DB-requests
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    token: Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_error = HTTPException(
        status_code = status.HTTP_401_UNNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str | None = payload.get("sub") # Attempts to retrieve ID from token created in auth.py
        if not user_id:
            raise credentials_error
    except JWTError:
        raise credentials_error

    # Compare id to database user
    # Shared HTTPException could make debugging harder
    user = db.get(User, int(user_id))
    if not user:
        raise credentials_error
    return user

