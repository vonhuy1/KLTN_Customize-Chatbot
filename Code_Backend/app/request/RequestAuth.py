from pydantic import BaseModel
from typing import Optional

class RequestLoginEmail(BaseModel):
    email: Optional[str]
    password: Optional[str]

class RequestLoginGoogle(BaseModel):
    email: Optional[str]
    token_google: Optional[str]

class RequestRefreshTokenLogin(BaseModel):
    refresh_token: Optional[str]

class RequestRegister(BaseModel):
    email: Optional[str]
    password: Optional[str]
    confirm_password: Optional[str]
    username: Optional[str]
