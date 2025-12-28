from uuid import UUID
from sqlalchemy.orm import Session
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryRepository:
    @staticmethod
    def create(db: Session, category: CategoryCreate, user_id: UUID | None = None) -> Category:
        """Create a new category"""
        db_category = Category(
            **category.model_dump(),
            user_id=user_id,
            is_default=user_id is None
        )
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category

    @staticmethod
    def get_by_id(db: Session, category_id: UUID) -> Category | None:
        """Get category by ID"""
        return db.query(Category).filter(Category.id == category_id).first()

    @staticmethod
    def get_all(db: Session, user_id: UUID | None = None, skip: int = 0, limit: int = 100) -> list[Category]:
        """Get all categories (default + user's custom categories)"""
        query = db.query(Category).filter(
            (Category.is_default == True) | (Category.user_id == user_id)
        )
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def get_user_categories(db: Session, user_id: UUID, skip: int = 0, limit: int = 100) -> list[Category]:
        """Get only user's custom categories"""
        return db.query(Category).filter(
            Category.user_id == user_id
        ).offset(skip).limit(limit).all()

    @staticmethod
    def update(db: Session, category_id: UUID, category_update: CategoryUpdate) -> Category | None:
        """Update a category"""
        db_category = CategoryRepository.get_by_id(db, category_id)
        if db_category:
            update_data = category_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_category, field, value)
            db.commit()
            db.refresh(db_category)
        return db_category

    @staticmethod
    def delete(db: Session, category_id: UUID) -> bool:
        """Delete a category"""
        db_category = CategoryRepository.get_by_id(db, category_id)
        if db_category:
            db.delete(db_category)
            db.commit()
            return True
        return False
