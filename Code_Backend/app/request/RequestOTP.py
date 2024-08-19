from pydantic import BaseModel
from typing import Optional

class RequestCreateOTP(BaseModel):
    email: Optional[str]

class RequestVerifyOTP(BaseModel):
    email: Optional[str]
    otp: Optional[str]