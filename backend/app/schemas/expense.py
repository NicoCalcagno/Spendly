from datetime import date, datetime
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.category import Category


class ExpenseBase(BaseModel):
    amount: Decimal = Field(..., gt=0, decimal_places=2)
    description: str = Field(..., min_length=1, max_length=255)
    expense_date: date
    payment_method: str = Field(..., min_length=1, max_length=50)
    notes: str | None = None


class ExpenseCreate(ExpenseBase):
    """Schema for creating a new expense"""
    category_id: UUID | None = None  # Optional: can be set by AI if not provided
    ai_suggested_category_id: UUID | None = None  # Set by AI service
    ai_confidence_score: float | None = None  # AI confidence (0.0-1.0)


class ExpenseUpdate(BaseModel):
    """Schema for updating an expense (all fields optional)"""
    amount: Decimal | None = Field(None, gt=0, decimal_places=2)
    description: str | None = Field(None, min_length=1, max_length=255)
    category_id: UUID | None = None
    expense_date: date | None = None
    payment_method: str | None = Field(None, min_length=1, max_length=50)
    notes: str | None = None


class ExpenseInDB(ExpenseBase):
    """Schema for expense as stored in database"""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    category_id: UUID | None
    ai_suggested_category_id: UUID | None
    ai_confidence_score: float | None
    created_at: datetime
    updated_at: datetime


class Expense(ExpenseBase):
    """Public expense schema with category details"""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    category_id: UUID | None
    category: Category | None = None
    ai_suggested_category_id: UUID | None
    ai_suggested_category: Category | None = None
    ai_confidence_score: float | None
    created_at: datetime
    updated_at: datetime


class ExpenseList(BaseModel):
    """Schema for paginated expense list"""
    items: list[Expense]
    total: int
    page: int
    page_size: int
    total_pages: int
