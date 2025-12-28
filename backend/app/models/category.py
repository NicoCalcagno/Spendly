from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    color = Column(String, nullable=False)  # Hex color (e.g., "#FF5733")
    icon = Column(String, nullable=False)  # Icon name for UI
    is_default = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="categories")
    expenses = relationship("Expense", foreign_keys="Expense.category_id", back_populates="category")
    ai_suggested_expenses = relationship("Expense", foreign_keys="Expense.ai_suggested_category_id", back_populates="ai_suggested_category")
