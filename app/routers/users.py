from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.utils.password import hash_password, verify_password
from app.auth.dependencies import get_current_user, require_admin
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/api/v1/users", tags=["users"])

class UserCreate(BaseModel):
    username: str
    password: str
    full_name: str
    email: str
    role: str = "driver"
    phone_number: Optional[str] = None
    driver_license: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    full_name: str
    email: str
    role: str
    is_admin: bool
    phone_number: Optional[str] = None
    driver_license: Optional[str] = None

class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str

# SPECIFIC ROUTES FIRST (before dynamic routes)
@router.put("/change-password")
async def change_password(
    request: PasswordChangeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not verify_password(request.current_password, current_user.hashed_password):
        raise HTTPException(status_code=401, detail="Current password is incorrect")
    
    current_user.hashed_password = hash_password(request.new_password)
    db.commit()
    
    return {"success": True, "message": "Password changed successfully. Please log in again."}

@router.get("/", response_model=List[UserResponse])
async def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    users = db.query(User).all()
    result = []
    for u in users:
        result.append(UserResponse(
            id=u.id,
            username=u.username,
            full_name=u.full_name or "",
            email=u.email,
            role=u.role if u.role else "driver",  # Handle NULL role
            is_admin=u.is_admin,
            phone_number=u.phone_number,
            driver_license=u.driver_license
        ))
    return result

@router.post("/", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    # Check if user exists
    existing = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    
    # Create new user
    db_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hash_password(user.password),
        role=user.role,
        is_admin=(user.role == "admin"),
        phone_number=user.phone_number,
        driver_license=user.driver_license,
        status="active"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return UserResponse(
        id=db_user.id,
        username=db_user.username,
        full_name=db_user.full_name or "",
        email=db_user.email,
        role=db_user.role if db_user.role else "driver",
        is_admin=db_user.is_admin,
        phone_number=db_user.phone_number,
        driver_license=db_user.driver_license
    )

# DYNAMIC ROUTES LAST
@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(
        id=user.id,
        username=user.username,
        full_name=user.full_name or "",
        email=user.email,
        role=user.role if user.role else "driver",
        is_admin=user.is_admin,
        phone_number=user.phone_number,
        driver_license=user.driver_license
    )

@router.put("/{user_id}")
async def update_user(
    user_id: int,
    user_update: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if "password" in user_update or "hashed_password" in user_update:
        raise HTTPException(status_code=400, detail="Use /change-password endpoint")
    
    for key, value in user_update.items():
        if hasattr(user, key) and key not in ["id", "hashed_password"]:
            setattr(user, key, value)
    
    db.commit()
    return {"message": "User updated"}

@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}
