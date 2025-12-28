from pydantic import BaseModel


class Token(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Data stored in JWT token"""
    user_id: str | None = None


class LoginRequest(BaseModel):
    """Login credentials"""
    email: str
    password: str
