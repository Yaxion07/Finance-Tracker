from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv()

from app.api.auth import router as auth_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to my Finance-tracker app!"}

@app.get("/health")
def health_check():
    return True

app.include_router(auth_router)