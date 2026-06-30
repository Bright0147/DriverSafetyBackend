from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str
    full_name: str
    email: str
    role: str = "driver"  #  Add role field with default
    is_admin: bool = False  # Keep for compatibility
    phone_number: Optional[str] = None
    driver_license: Optional[str] = None
