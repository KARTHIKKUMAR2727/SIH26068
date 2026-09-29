from typing import Optional
from pydantic import BaseModel, EmailStr

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    preferred_language: Optional[str] = "en"
    preferred_units: Optional[str] = "metric"
    default_location: Optional[str] = "Chennai, Tamil Nadu, India"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserProfile(BaseModel):
    id: str
    name: str
    email: EmailStr
    preferred_language: str
    preferred_units: str
    default_location: str
    created_at: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    preferred_language: Optional[str] = None
    preferred_units: Optional[str] = None
    default_location: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserProfile
