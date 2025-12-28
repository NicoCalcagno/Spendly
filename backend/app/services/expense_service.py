from uuid import UUID
from sqlalchemy.orm import Session
from app.repositories.expense_repository import ExpenseRepository
from app.schemas.expense import ExpenseCreate, ExpenseUpdate
from app.models.expense import Expense
from app.services.ai_service import AIService
from app.config import get_settings

settings = get_settings()


class ExpenseService:
    @staticmethod
    def create_expense(db: Session, expense: ExpenseCreate, user_id: UUID) -> Expense:
        """
        Create a new expense.
        If category_id is not provided and AI is configured, use AI to suggest category.
        """
        expense_data = expense.model_dump()

        # If no category provided and AI is available, use AI to suggest
        if not expense_data.get("category_id") and settings.ANTHROPIC_API_KEY:
            try:
                ai_service = AIService()
                suggested_category_id, confidence = ai_service.categorize_expense(
                    db=db,
                    description=expense_data["description"],
                    amount=expense_data["amount"],
                    user_id=user_id
                )

                if suggested_category_id and confidence > 0.5:
                    expense_data["ai_suggested_category_id"] = suggested_category_id
                    expense_data["ai_confidence_score"] = confidence
                    expense_data["category_id"] = suggested_category_id

            except Exception as e:
                print(f"AI categorization failed: {e}")

        # Create expense with original or AI-suggested category
        expense_create = ExpenseCreate(**expense_data)
        return ExpenseRepository.create(db, expense_create, user_id)

    @staticmethod
    def get_expense(db: Session, expense_id: UUID, user_id: UUID) -> Expense | None:
        """Get an expense by ID (only if it belongs to the user)"""
        return ExpenseRepository.get_by_id(db, expense_id, user_id)

    @staticmethod
    def list_expenses(
        db: Session,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100,
        category_id: UUID | None = None
    ) -> tuple[list[Expense], int]:
        """
        List all expenses for a user with pagination.
        Returns (expenses, total_count).
        """
        return ExpenseRepository.get_all(db, user_id, skip, limit, category_id)

    @staticmethod
    def update_expense(db: Session, expense_id: UUID, user_id: UUID, expense_update: ExpenseUpdate) -> Expense | None:
        """Update an expense (only if it belongs to the user)"""
        return ExpenseRepository.update(db, expense_id, user_id, expense_update)

    @staticmethod
    def delete_expense(db: Session, expense_id: UUID, user_id: UUID) -> bool:
        """Delete an expense (only if it belongs to the user)"""
        return ExpenseRepository.delete(db, expense_id, user_id)
