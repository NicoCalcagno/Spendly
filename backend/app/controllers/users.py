from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.services.user_service import UserService
from app.schemas.user import User, UserCreate
from app.models.user import User as UserModel

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """Register a new user"""
    try:
        return UserService.create_user(db, user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/me", response_model=User)
def get_my_profile(
    current_user: UserModel = Depends(get_current_user)
):
    """Get current user profile (requires authentication)"""
    return current_user


@router.get("/{user_id}", response_model=User)
def get_user(
    user_id: UUID,
    db: Session = Depends(get_db)
):
    """Get user by ID (admin only)"""
    user = UserService.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
