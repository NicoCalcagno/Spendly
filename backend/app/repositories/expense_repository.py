from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate, ExpenseUpdate


class ExpenseRepository:
    @staticmethod
    def create(db: Session, expense: ExpenseCreate, user_id: UUID) -> Expense:
        """Create a new expense"""
        db_expense = Expense(
            **expense.model_dump(),
            user_id=user_id
        )
        db.add(db_expense)
        db.commit()
        db.refresh(db_expense)
        return db_expense

    @staticmethod
    def get_by_id(db: Session, expense_id: UUID, user_id: UUID) -> Expense | None:
        """Get expense by ID (with category relationships loaded)"""
        return db.query(Expense).options(
            joinedload(Expense.category),
            joinedload(Expense.ai_suggested_category)
        ).filter(
            Expense.id == expense_id,
            Expense.user_id == user_id
        ).first()

    @staticmethod
    def get_all(
        db: Session,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100,
        category_id: UUID | None = None
    ) -> tuple[list[Expense], int]:
        """Get all expenses for a user with optional filtering"""
        query = db.query(Expense).options(
            joinedload(Expense.category),
            joinedload(Expense.ai_suggested_category)
        ).filter(Expense.user_id == user_id)

        # Optional category filter
        if category_id:
            query = query.filter(Expense.category_id == category_id)

        # Get total count
        total = query.count()

        # Get paginated results
        expenses = query.order_by(Expense.expense_date.desc()).offset(skip).limit(limit).all()

        return expenses, total

    @staticmethod
    def update(db: Session, expense_id: UUID, user_id: UUID, expense_update: ExpenseUpdate) -> Expense | None:
        """Update an expense"""
        db_expense = ExpenseRepository.get_by_id(db, expense_id, user_id)
        if db_expense:
            update_data = expense_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_expense, field, value)
            db.commit()
            db.refresh(db_expense)
        return db_expense

    @staticmethod
    def delete(db: Session, expense_id: UUID, user_id: UUID) -> bool:
        """Delete an expense"""
        db_expense = ExpenseRepository.get_by_id(db, expense_id, user_id)
        if db_expense:
            db.delete(db_expense)
            db.commit()
            return True
        return False
