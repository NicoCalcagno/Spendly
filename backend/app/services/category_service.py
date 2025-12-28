from uuid import UUID
from sqlalchemy.orm import Session
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.models.category import Category


class CategoryService:
    @staticmethod
    def create_category(db: Session, category: CategoryCreate, user_id: UUID | None = None) -> Category:
        """
        Create a new category.
        If user_id is None, creates a default (system) category.
        """
        return CategoryRepository.create(db, category, user_id)

    @staticmethod
    def get_category(db: Session, category_id: UUID) -> Category | None:
        """Get a category by ID"""
        return CategoryRepository.get_by_id(db, category_id)

    @staticmethod
    def list_categories(db: Session, user_id: UUID | None = None, skip: int = 0, limit: int = 100) -> list[Category]:
        """
        List all available categories for a user.
        Returns default categories + user's custom categories.
        """
        return CategoryRepository.get_all(db, user_id, skip, limit)

    @staticmethod
    def update_category(db: Session, category_id: UUID, category_update: CategoryUpdate, user_id: UUID | None = None) -> Category | None:
        """
        Update a category.
        Users can only update their own categories, not default ones.
        """
        category = CategoryRepository.get_by_id(db, category_id)
        if not category:
            return None

        # Don't allow updating default categories
        if category.is_default:
            raise ValueError("Cannot update default categories")

        # Check if user owns this category
        if category.user_id and category.user_id != user_id:
            raise PermissionError("Cannot update another user's category")

        return CategoryRepository.update(db, category_id, category_update)

    @staticmethod
    def delete_category(db: Session, category_id: UUID, user_id: UUID | None = None) -> bool:
        """
        Delete a category.
        Users can only delete their own categories.
        Note: Expenses referencing this category will have category_id set to NULL (handled by DB with ON DELETE SET NULL).
        """
        category = CategoryRepository.get_by_id(db, category_id)
        if not category:
            return False

        # Don't allow deleting default categories
        if category.is_default:
            raise ValueError("Cannot delete default categories")

        # Check if user owns this category
        if category.user_id and category.user_id != user_id:
            raise PermissionError("Cannot delete another user's category")

        return CategoryRepository.delete(db, category_id)
