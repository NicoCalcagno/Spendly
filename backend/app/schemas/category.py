from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = None
    color: str = Field(..., pattern=r"^#[0-9A-Fa-f]{6}$")  # Hex color validation
    icon: str = Field(..., min_length=1, max_length=50)


class CategoryCreate(CategoryBase):
    """Schema for creating a new category"""
    pass


class CategoryUpdate(BaseModel):
    """Schema for updating a category (all fields optional)"""
    name: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = None
    color: str | None = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    icon: str | None = Field(None, min_length=1, max_length=50)


class CategoryInDB(CategoryBase):
    """Schema for category as stored in database"""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID | None
    is_default: bool
    created_at: datetime


class Category(CategoryBase):
    """Public category schema"""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    is_default: bool
    created_at: datetime
