from pydantic import BaseModel
from typing import List

class ListUserChat(BaseModel):
    id: int
    email: str
    chat_name: str

class ChatDetail(BaseModel):
    id: int
    chat_id: int
    question: str
    answer: str
    data_relevant: str
    source_file: str

class ChatDetailById(BaseModel):
    id: int
    data_relevant: str
    source_file: str

class ListChatDeTail(BaseModel):
    detail_chat: List[ChatDetail]

class UserInfoListResponse(BaseModel):
    chat: List[ListUserChat]

class Message(BaseModel):
    message: str
   
class CheckModel(BaseModel):
    check: bool

class ResponseRenderChatHistory(BaseModel):
    status: int
    data: UserInfoListResponse

class ResponseChatDetailById(BaseModel):
    status: int
    data: ChatDetailById
    
class ResponseLoadChatHistory(BaseModel):
    status: int
    data: ListChatDeTail

class ResponseEditChat(BaseModel):
    status: int
    data: Message

class ResponseDeleteChat(BaseModel):
    status: int
    data: Message

class ResponseCreateChat(BaseModel):
    status: int
    data: Message

class ResponseStopChat(BaseModel):
    status: int
    data: Message
    
class ResponseDeleteChatDetailById(BaseModel):
    status: int
    data: CheckModel

class ReponseError(BaseModel):
    status: int
    data: Message