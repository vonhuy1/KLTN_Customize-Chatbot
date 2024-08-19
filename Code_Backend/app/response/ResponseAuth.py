from pydantic import BaseModel
from typing import List, Union, Optional
class Message(BaseModel):
    message: str
class DataLogin(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    session_id: str

class CheckModel(BaseModel):
    check: bool

class DataRefreshToken(BaseModel):
    token_new: str
    session_id: str

class ResponseCreateOTP(BaseModel):
    status: int
    data: CheckModel
    otp: str

class ResponseLoginGoogle(BaseModel):
    status: int
    data: DataLogin

class ResponseRefreshToken(BaseModel):
    status: int
    data: DataRefreshToken

class DataSignUp(BaseModel):
    email: str

class ResponseRegister(BaseModel):
    status: int
    data: DataSignUp

class ReponseError(BaseModel):
    status: int
    data: Message