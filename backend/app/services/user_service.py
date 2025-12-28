from uuid import UUID
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password"""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        """
        Create a new user.
        Raises ValueError if email already exists.
        """
        # Check if user already exists
        existing_user = UserRepository.get_by_email(db, user.email)
        if existing_user:
            raise ValueError("Email already registered")

        hashed_password = UserService.hash_password(user.password)
        return UserRepository.create(db, user, hashed_password)

    @staticmethod
    def get_user(db: Session, user_id: UUID) -> User | None:
        """Get a user by ID"""
        return UserRepository.get_by_id(db, user_id)

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User | None:
        """Get a user by email"""
        return UserRepository.get_by_email(db, email)

    @staticmethod
    def update_user(db: Session, user_id: UUID, user_update: UserUpdate) -> User | None:
        """Update a user"""
        hashed_password = None
        if user_update.password:
            hashed_password = UserService.hash_password(user_update.password)

        return UserRepository.update(db, user_id, user_update, hashed_password)

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> User | None:
        """
        Authenticate a user.
        Returns the user if credentials are valid, None otherwise.
        """
        user = UserRepository.get_by_email(db, email)
        if not user:
            return None
        if not UserService.verify_password(password, user.hashed_password):
            return None
        return user
