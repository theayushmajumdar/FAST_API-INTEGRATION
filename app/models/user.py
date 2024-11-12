from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    Phone_Number: str = Field(..., min_length=10, max_length=10)
    FName: str
    LName: str
    Email: str
    Course: str
    Country: str
    Gender: str

class UserUpdate(BaseModel):
    FName: Optional[str] = None
    LName: Optional[str] = None
    Email: Optional[str] = None
    Course: Optional[str] = None
    Country: Optional[str] = None
    Gender: Optional[str] = None