from pydantic import BaseModel

class Message(BaseModel):
    message: str

class CheckModel(BaseModel):
    check: bool

class ResponseCreateOTP(BaseModel):
    status: int
    data: CheckModel
    otp: str

class ResponseVerifyOTP(BaseModel):
    status: int
    data: Message
    newpassword: str

class ResponseVerifyOTPSignUp(BaseModel):
    status: int
    data: Message

class ReponseError(BaseModel):
    status: int
    data: Message