from pydantic import BaseModel, condecimal
from datetime import date
from typing import Optional

class TransactionBase(BaseModel):
    amount: condecimal(max_digits=12, decimal_places=2)
    description: Optional[str] = None
    date: date
    category_id: Optional[int] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    amount: Optional[condecimal(max_digits=12, decimal_places=2)] = None
    description: Optional[str] = None
    date: Optional[date] = None
    category_id: Optional[int] = None

class TransactionOut(TransactionBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True