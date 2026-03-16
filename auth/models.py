"""Pydantic models for request/response validation"""
from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    """User creation request model"""
    email: EmailStr
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "strongpassword123"
            }
        }


class UserLogin(BaseModel):
    """User login request model"""
    email: EmailStr
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "strongpassword123"
            }
        }


class User(BaseModel):
    """User response model"""
    email: EmailStr
    is_active: bool
    role: Optional[str] = "GENERAL"
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "is_active": True,
                "role": "GENERAL"
            }
        }


class Token(BaseModel):
    """Token response model"""
    access_token: str
    token_type: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }


class TokenData(BaseModel):
    """Token data model (decoded token payload)"""
    email: Optional[str] = None
