from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.transaction import Transaction
from app.schemas.transactionschema import TransactionCreate, TransactionUpdate, TransactionOut
from app.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("/", response_model=TransactionOut, status_code=status.HTTP_201_CREATED)
def create_transaction(payload: TransactionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    trans = Transaction(
        amount=payload.amount,
        description=payload.description,
        date=payload.date,
        user_id=current_user.id,
        category_id=payload.category_id,
    )
    db.add(trans)
    db.commit()
    db.refresh(trans)
    return trans

@router.get("/", response_model=List[TransactionOut], status_code=status.HTTP_200_OK)
def list_transactions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Transaction).filter(Transaction.user_id == current_user.id).order_by(Transaction.date.desc()).all()

@router.get("/{transaction_id}", response_model=TransactionOut)
def get_transaction(transaction_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    trans = db.query(Transaction).filter(Transaction.user_id == current_user.id, Transaction.id == transaction_id).first()
    if not trans:
        raise HTTPException(status_code=404, detail="Transaction coult not be found.")
    return trans

@router.put("/{transaction_id}", response_model=TransactionOut)
def update_transaction(transaction_id: int, payload: TransactionUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    trans = db.query(Transaction).filter(Transaction.user_id == current_user.id, Transaction.id == transaction_id).first()
    if not trans:
        raise HTTPException(status_code=404, detail="Transaction coult not be found.")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(trans, field, value)
    db.commit()
    db.refresh(trans)
    return trans

@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(transaction_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    trans = db.query(Transaction).filter(Transaction.user_id == current_user.id, Transaction.id == transaction_id).first()
    if not trans:
        raise HTTPException(status_code=404, detail="Transaction coult not be found.")
    db.delete(trans)
    db.commit()
    return None

    