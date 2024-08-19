from pydantic import BaseModel
from typing import List

class Message(BaseModel):
    message: str

class CheckModel(BaseModel):
    check: bool

class DataGetNameFile(BaseModel):
    files: List[str]

class ResponseGetNameFile(BaseModel):
    status: int
    data: DataGetNameFile

class ResponseDeleteFile(BaseModel):
    status: int
    data: Message

class ResponseDownloadFolder(BaseModel):
    status: int
    data: Message

class ResponseDeleteAllFile(BaseModel):
    status: int
    data: Message

class ResponseDownloadFile(BaseModel):
     status: int
     data: Message

class ResponseUploadedFile(BaseModel):
     status: int
     data: Message

class ReponseError(BaseModel):
    status: int
    data: Message