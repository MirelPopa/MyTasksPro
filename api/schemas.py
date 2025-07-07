from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class CreateTask(BaseModel):
    title: str
    priority: int = 1
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.now)
    completed: Optional[bool] = False

class TaskUpdate(BaseModel):
    title: str
    priority: int
    description: Optional[str]
    due_date: Optional[datetime]
    completed: Optional[bool]
