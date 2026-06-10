from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str
    full_name: str
    email: str
    is_admin: bool = False
    phone_number: Optional[str] = None
    driver_license: Optional[str] = None