from pydantic import BaseModel, EmailStr

class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str

class UserReadSchema(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True # This allows the model to read attributes from the SQLAlchemy model directly