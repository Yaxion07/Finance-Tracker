from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    # Foreign key to the user who created the category
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # One user can't have two categories with the same name
    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_categories_user_name"),
    )

    transactions = relationship("Transaction", back_populates="category", passive_deletes=True)