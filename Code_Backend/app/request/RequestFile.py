from pydantic import BaseModel
from typing import List, Optional
from fastapi import UploadFile
class RequestGetNameFile(BaseModel):
    user_id: Optional[str]
class RequestDeleteFile(BaseModel):
    user_id: Optional[str]
    name_file: Optional[str]
class RequestDeleteAllFile(BaseModel):
    user_id: Optional[str]
class RequestDownLoadFolder(BaseModel):
    user_id: Optional[str]

class RequestDownLoadFile(BaseModel):
    user_id: Optional[str]
    name_file: Optional[str]
class RequestUploadFile(BaseModel):
    files: Optional[List[UploadFile]] = None
    user_id: Optional[str]