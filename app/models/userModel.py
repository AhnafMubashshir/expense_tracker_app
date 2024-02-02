from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    name: str
    email: str
    age: int

class RegisteredUser(BaseModel):
    id: Optional[int]
    name: Optional[str]
    email: Optional[str]
    age: Optional[int]

class UpdateUserRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None


class UpdateUserResponse(User):
    pass