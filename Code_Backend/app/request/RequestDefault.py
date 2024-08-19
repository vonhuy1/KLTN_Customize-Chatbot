from pydantic import BaseModel, EmailStr
from typing import Optional, List
from fastapi import UploadFile
class RequestCreateFireBaseUserGoogle(BaseModel):
    email: Optional[str] = None
    token_google: Optional[str] = None
class RequestInfoUser(BaseModel):
    user_id: str
class RequestIsMe(BaseModel):
    token: Optional[str]

class RequestUpLoadImage(BaseModel):
    user_id: Optional[str]
    files: UploadFile = None
