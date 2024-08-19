from pydantic import BaseModel
from typing import Optional
class RequestLoginEmail(BaseModel):
    email: Optional[str]
    password: Optional[str]

class RequestLoginGoogle(BaseModel):
    email: Optional[str]
    token_google: Optional[str]
class RequestUpdateUserInfo(BaseModel):
    user_id: Optional[str]
    uid: Optional[str]
    email: Optional[str]
    display_name: Optional[str]
    photo_url: Optional[str]

class RequestCheckInfoGoogle(BaseModel):
    user_id: int
class RequestCheckInfoGoogleEmail(BaseModel):
   email:Optional[str]
class RequestCreateOTP(BaseModel):
    email: Optional[str]

class RequestVerifyOTP(BaseModel):
    email: Optional[str]
    otp: Optional[str]
        
class RequestCheckStateLogin(BaseModel):
    user_id: Optional[int]
    session_id_now: Optional[str]

class RequestSignUp(BaseModel):
    email: Optional[str]
    password: Optional[str]
    confirm_password: Optional[str]
    username: Optional[str]

class RequestResetPassword(BaseModel):
    email: Optional[str]

class RequestChangePassword(BaseModel):
    user_id: Optional[str]
    current_password: Optional[str]
    new_password: Optional[str]
    confirm_new_password: Optional[str]

class RequestRefreshTokenLogin(BaseModel):
    refresh_token: Optional[str]