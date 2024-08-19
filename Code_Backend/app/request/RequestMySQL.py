from pydantic import BaseModel
from typing import Optional

class RequestRenderChatHistory(BaseModel):
    user_id: Optional[int]

class RequestLoadChatHistory(BaseModel):
    user_id: Optional[int]
    chat_id: Optional[int]

class RequestGetChatDetails(BaseModel):
    id: Optional[str]

class RequestStopChat(BaseModel):
    user_id: Optional[str]
    chat_name: Optional[str]

class RequestCreateChatHistory(BaseModel):
    user_id: Optional[str]
    chat_name: Optional[str]
class RequestEditNameChat(BaseModel):
    user_id: Optional[str]
    name_old: Optional[str]
    name_new: Optional[str]

class RequestDeleteChat(BaseModel):
    user_id: Optional[str]
    chat_name: Optional[str]

class RequestDeleteDetailChat(BaseModel):
    user_id: Optional[str]
    id_chat_detail: Optional[str]