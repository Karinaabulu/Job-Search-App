from pydantic import BaseModel
from typing import Optional

class NINSubmit(BaseModel):
    nin: str

class UserResponse(BaseModel):
    id: int
    nin: str
    full_name: str
    date_of_birth: str
    desired_job: Optional[str] = None
    payment_status: str

    class Config:
        from_attributes = True

class JobPreference(BaseModel):
    desired_job: str

