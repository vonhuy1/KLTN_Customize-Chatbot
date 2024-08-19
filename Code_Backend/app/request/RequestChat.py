from pydantic import BaseModel
from typing import Optional

class RequestQuery2UpgradeOld(BaseModel):
    user_id: int
    text_all: str
    question: Optional[str]
    chat_name: Optional[str]

class RequestExtractFile(BaseModel):
    user_id: int

class RequestDeleteChat(BaseModel):
    user_id: int
    chat_name: Optional[str]
class RequestGenerateQuestion(BaseModel):
    user_id: int