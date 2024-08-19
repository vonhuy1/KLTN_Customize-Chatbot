from pydantic import BaseModel
from typing import List, Union, Optional

class DataAnswer(BaseModel):
    answer: str

class DataAnswer1(BaseModel):
    id: int
    answer: str
    data_relevant: List[str]
    sources: List[str]

class FileMetadata(BaseModel):
    source: str

class FileResponse(BaseModel):
    page_content: str
    metadata: FileMetadata
    type: str

class DataExtractFile(BaseModel):
   text_all: Union[List[FileResponse], None, str]

class Message(BaseModel):
    message: str
   
class CheckModel(BaseModel):
    check: bool

class ResponseQuery2Upgrade(BaseModel):
    status: int
    data: DataAnswer

class GenerateQuestion(BaseModel):
    question: Union[List[str], bool]

class ResponseGenerateQuestion(BaseModel):
    status: int
    data: GenerateQuestion

class ResponseQuery2UpgradeOld(BaseModel):
    status: int
    data: DataAnswer1

class ResponseExtractFile(BaseModel):
    status: int
    data: DataExtractFile

class ResponseDeleteChat(BaseModel):
    status: int
    data: Message
    
class ReponseError(BaseModel):
    status: int
    data: Message