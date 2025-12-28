from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user_id
from app.services.expense_service import ExpenseService
from app.schemas.expense import Expense, ExpenseCreate, ExpenseUpdate, ExpenseList
from math import ceil

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.post("/", response_model=Expense, status_code=status.HTTP_201_CREATED)
def create_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id)
):
    """Create a new expense (requires authentication)"""
    return ExpenseService.create_expense(db, expense, user_id)


@router.get("/", response_model=ExpenseList)
def list_expenses(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category_id: UUID | None = None,
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id)
):
    """List all expenses with pagination (requires authentication)"""
    expenses, total = ExpenseService.list_expenses(
        db, user_id, skip, limit, category_id
    )

    return ExpenseList(
        items=expenses,
        total=total,
        page=skip // limit + 1,
        page_size=limit,
        total_pages=ceil(total / limit) if total > 0 else 0
    )


@router.get("/{expense_id}", response_model=Expense)
def get_expense(
    expense_id: UUID,
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id)
):
    """Get a specific expense by ID (requires authentication)"""
    expense = ExpenseService.get_expense(db, expense_id, user_id)
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    return expense


@router.put("/{expense_id}", response_model=Expense)
def update_expense(
    expense_id: UUID,
    expense_update: ExpenseUpdate,
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id)
):
    """Update an expense (requires authentication)"""
    expense = ExpenseService.update_expense(db, expense_id, user_id, expense_update)
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    return expense


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: UUID,
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id)
):
    """Delete an expense (requires authentication)"""
    success = ExpenseService.delete_expense(db, expense_id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
