from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict, Field
from src.auth.models import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str | None = None
    
class UserResponse(BaseModel):
    id: int
    full_name: str | None
    role: UserRole
    is_active: bool
    created_at: datetime
    
    # This tells Pydantic to read data from SQLAlchemy model
    model_config = ConfigDict(from_attributes=True)
    
class Token(BaseModel):
    access_token: str
    token_type: str
    

class TokenData(BaseModel):
    sub: Optional[str] = None
