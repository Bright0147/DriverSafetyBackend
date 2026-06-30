from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.utils.password import hash_password
from pydantic import BaseModel
import secrets
from datetime import datetime, timedelta
import os

router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])

class ForgotPasswordRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """Request password reset - stores token in database"""
    user = db.query(User).filter(User.email == request.email).first()
    
    # Always return success (security: don't reveal if email exists)
    if not user:
        return {"message": "If email exists, reset link will be sent", "success": True}
    
    # Generate reset token (expires in 1 hour)
    token = secrets.token_urlsafe(32)
    expiry = datetime.utcnow() + timedelta(hours=1)
    
    # Save token to database
    user.reset_token = token
    user.reset_token_expiry = expiry
    db.commit()
    
    # In production, send email here
    # For now, return token in response (for testing)
    print(f"🔐 Reset token for {user.email}: {token}")
    print(f"🔗 Reset link: https://driversafetybackend.onrender.com/reset-password?token={token}")
    
    return {
        "message": "Reset link sent to email",
        "success": True,
        "token": token  # Remove in production - only for testing
    }

@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    """Reset password using token from database"""
    # Find user by token
    user = db.query(User).filter(User.reset_token == request.token).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid or expired token"
        )
    
    # Check if token is expired
    if user.reset_token_expiry and datetime.utcnow() > user.reset_token_expiry:
        # Clear expired token
        user.reset_token = None
        user.reset_token_expiry = None
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Token expired"
        )
    
    # Update password
    try:
        user.hashed_password = hash_password(request.new_password)
        # Clear the used token
        user.reset_token = None
        user.reset_token_expiry = None
        db.commit()
        
        return {"message": "Password reset successfully", "success": True}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_ERROR, 
            detail=str(e)
        )

@router.get("/verify-token/{token}")
async def verify_token(token: str, db: Session = Depends(get_db)):
    """Verify if a token is valid (for the reset page)"""
    user = db.query(User).filter(User.reset_token == token).first()
    
    if not user:
        return {"valid": False, "message": "Invalid token"}
    
    if user.reset_token_expiry and datetime.utcnow() > user.reset_token_expiry:
        # Clear expired token
        user.reset_token = None
        user.reset_token_expiry = None
        db.commit()
        return {"valid": False, "message": "Token expired"}
    
    return {"valid": True, "message": "Token is valid"}
