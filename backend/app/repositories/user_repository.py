from uuid import UUID
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserRepository:
    @staticmethod
    def create(db: Session, user: UserCreate, hashed_password: str) -> User:
        """Create a new user"""
        db_user = User(
            email=user.email,
            full_name=user.full_name,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_by_id(db: Session, user_id: UUID) -> User | None:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_by_email(db: Session, email: str) -> User | None:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def update(db: Session, user_id: UUID, user_update: UserUpdate, hashed_password: str | None = None) -> User | None:
        """Update a user"""
        db_user = UserRepository.get_by_id(db, user_id)
        if db_user:
            update_data = user_update.model_dump(exclude_unset=True, exclude={"password"})
            for field, value in update_data.items():
                setattr(db_user, field, value)

            if hashed_password:
                db_user.hashed_password = hashed_password

            db.commit()
            db.refresh(db_user)
        return db_user

    @staticmethod
    def delete(db: Session, user_id: UUID) -> bool:
        """Delete a user"""
        db_user = UserRepository.get_by_id(db, user_id)
        if db_user:
            db.delete(db_user)
            db.commit()
            return True
        return False
