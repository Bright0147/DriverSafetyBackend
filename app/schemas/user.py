from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str
    full_name: str
    email: str
    role: str = "driver"  # ✅ Add this field
    is_admin: bool = False  # Keep for compatibility
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
