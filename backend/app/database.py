import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

DATABASE_URL = os.getenv("DATABASE_URL")

# Base class for our models
Base = declarative_base()

engine = create_engine(DATABASE_URL) if DATABASE_URL else None

# Used later to create db-sessions in Routes/Services, but only if engine is not None
SessionLocal = (
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
    if engine else None
)
