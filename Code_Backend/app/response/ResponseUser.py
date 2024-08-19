from pydantic import BaseModel

class DataLogin(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    session_id: str

class DataRefreshToken(BaseModel):
    token_new: str
    session_id: str

class DataSignUp(BaseModel):
    email: str

class Message(BaseModel):
    message: str

class CheckModel(BaseModel):
    check: bool

class ResponseLoginEmail(BaseModel):
    status: int
    data: DataLogin

class ResponseLoginGoogle(BaseModel):
    status: int
    data: DataLogin

class ResponseUpdateUserInfo(BaseModel):
    status : int
    data: Message

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

class ResponseCheckInfoGoogle(BaseModel):
    status: int
    data: CheckModel

class ResponseCheckStateLogin(BaseModel):
    status: int
    data: CheckModel

class ResponseSignUp(BaseModel):
    status: int
    data: DataSignUp

class ResponseResetPassword(BaseModel):
    status: int
    data: Message

class ResponseChangePassword(BaseModel):
    status: int
    data: Message

class ResponseRefreshTokenLogin(BaseModel):
    status: int
    data: DataRefreshToken

class ReponseError(BaseModel):
    status: int
    data: Message