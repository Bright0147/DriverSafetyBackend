from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.utils.password import verify_password
from app.auth.dependencies import create_access_token
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    user_id: int
    username: str
    full_name: str
    email: str
    is_admin: bool
    role: str
    access_token: str
    token_type: str
    message: str

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    print("=== LOGIN ATTEMPT ===")
    print(f"Username: {request.username}")
    
    user = db.query(User).filter(
        (User.username == request.username) | (User.email == request.username)
    ).first()

    if not user:
        print("User not found")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    print(f"User found: {user.username}")
    
    result = verify_password(request.password, user.hashed_password)
    print(f"Verify result: {result}")
    
    if not result:
        print("Password mismatch - rejecting")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create JWT token
    access_token = create_access_token(data={"sub": str(user.id)})
    
    print("Login successful")
    return LoginResponse(
        success=True,
        user_id=user.id,
        username=user.username,
        full_name=user.full_name or user.username,
        email=user.email,
        is_admin=user.is_admin,
        role=user.role if hasattr(user, 'role') else ("admin" if user.is_admin else "driver"),
        access_token=access_token,
        token_type="bearer",
        message="Login successful"
    )
