from sqlalchemy import CheckConstraint, Column, ForeignKey, Index, Integer, Numeric, String, Date
from sqlalchemy.orm import relationship

from app.database import Base 

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Numeric(12, 2), nullable=False)
    description = Column(String, nullable=True)
    date = Column(Date, nullable=False)  # Sets the default date to current time

    # Foreign key to the user who created the transaction
    user_id = Column(
    Integer,
    ForeignKey("users.id", ondelete="CASCADE"),
    nullable=False,
    index=True,
    )

    # Foreign key to the category of the transaction
    category_id = Column(
    Integer,
    ForeignKey("categories.id", ondelete="SET NULL"),
    nullable=True,
    index=True,
    )

    # Relationship to the User model
    user = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions", lazy="joined", uselist=False)

    # Index for faster querying by user and date
    __table_args__ = (
        Index("ix_txn_user_date", "user_id", "date"),
        CheckConstraint("amount <> 0", name="ck_transactions_amount_nonzero"),
    )