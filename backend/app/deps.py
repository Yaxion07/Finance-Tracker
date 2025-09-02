from app.database import SessionLocal
from sqlalchemy.orm import Session

# Returns a DB session that closes automatically. Used when handling DB-requests
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()