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

# Store reset tokens (in production, use Redis or database)
# For Render free tier, this works but tokens reset on restart
reset_tokens = {}

class ForgotPasswordRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """Request password reset - sends reset link to email"""
    user = db.query(User).filter(User.email == request.email).first()
    
    # Always return success (security: don't reveal if email exists)
    if not user:
        return {"message": "If email exists, reset link will be sent", "success": True}
    
    # Generate reset token (expires in 1 hour)
    token = secrets.token_urlsafe(32)
    expiry = datetime.utcnow() + timedelta(hours=1)
    reset_tokens[token] = {"user_id": user.id, "expiry": expiry}
    
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
    """Reset password using token"""
    token_data = reset_tokens.get(request.token)
    
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid or expired token"
        )
    
    if datetime.utcnow() > token_data["expiry"]:
        del reset_tokens[request.token]
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Token expired"
        )
    
    # Update password
    try:
        user = db.query(User).filter(User.id == token_data["user_id"]).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="User not found"
            )
        
        user.hashed_password = hash_password(request.new_password)
        db.commit()
        
        # Delete used token
        del reset_tokens[request.token]
        
        return {"message": "Password reset successfully", "success": True}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_ERROR, 
            detail=str(e)
        )
    finally:
        db.close()

@router.get("/verify-token/{token}")
async def verify_token(token: str):
    """Verify if a token is valid (for the reset page)"""
    token_data = reset_tokens.get(token)
    
    if not token_data:
        return {"valid": False, "message": "Invalid token"}
    
    if datetime.utcnow() > token_data["expiry"]:
        return {"valid": False, "message": "Token expired"}
    
    return {"valid": True, "message": "Token is valid"}
