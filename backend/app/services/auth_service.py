from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from uuid import UUID
from app.config import get_settings

settings = get_settings()


class AuthService:
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Create a JWT access token.

        Args:
            data: Dictionary to encode in the token (e.g., {"sub": user_id})
            expires_delta: Optional custom expiration time

        Returns:
            Encoded JWT token
        """
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

        return encoded_jwt

    @staticmethod
    def verify_token(token: str) -> Optional[str]:
        """
        Verify and decode a JWT token.

        Args:
            token: JWT token to verify

        Returns:
            User ID (sub claim) if valid, None otherwise
        """
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                return None
            return user_id
        except JWTError:
            return None

    @staticmethod
    def create_user_token(user_id: UUID) -> dict:
        """
        Create an access token for a user.

        Args:
            user_id: User UUID

        Returns:
            Dictionary with access_token and token_type
        """
        access_token = AuthService.create_access_token(
            data={"sub": str(user_id)}
        )
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
