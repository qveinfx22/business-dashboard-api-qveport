from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    full_name: str


class UserCreate(UserBase):
    password: str
    is_admin: bool = False


class UserRead(UserBase):
    id: int
    is_admin: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
