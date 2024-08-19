from pydantic import BaseModel

class DataInfoUser(BaseModel):
    uid: str
    email: str
    display_name: str
    photo_url: str

class DataIsMe(BaseModel):
    user_id: int

class DataUploadImage(BaseModel):
    url: str
class Message(BaseModel):
    message: str
   
class CheckModel(BaseModel):
    check: bool

class DataCreateFireBaseUser(BaseModel):
    localId: str
    email: str
    displayName: str
    photoUrl: str

class ResponseCreateFireBaseUser(BaseModel):
    status: int
    data: DataCreateFireBaseUser

class ResponseInfoUser(BaseModel):
    status: int
    data: DataInfoUser

class ResponseIsMe(BaseModel):
    status: int
    data: DataIsMe

class ResponseUploadImage(BaseModel):
    status: int
    data: DataUploadImage

class ReponseError(BaseModel):
    status: int
    data: Message