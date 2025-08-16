from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from app.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) # Sets the default date to current time

    transactions = relationship(
        "Transaction",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    

