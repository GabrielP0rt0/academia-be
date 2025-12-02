"""
Authentication routes.

Simple hardcoded authentication for POC purposes.
"""
from fastapi import APIRouter, HTTPException
from app.schemas import LoginRequest, LoginResponse
from app import db

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# Hardcoded credentials for POC
HARDCODED_EMAIL = "admin@academia.com"
HARDCODED_PASSWORD = "admin123"


@router.post("/login", response_model=LoginResponse, status_code=200)
async def login(credentials: LoginRequest):
    """
    Simple login endpoint with hardcoded credentials.
    
    For POC purposes only. In production, use proper authentication.
    """
    if credentials.email == HARDCODED_EMAIL and credentials.password == HARDCODED_PASSWORD:
        # Generate simple token (in production, use JWT)
        token = "hardcoded_token_for_poc_12345"
        return LoginResponse(token=token, message="Login successful")
    
    raise HTTPException(
        status_code=401,
        detail="Invalid email or password"
    )

