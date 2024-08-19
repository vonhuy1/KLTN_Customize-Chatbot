import json

from request import RequestMySQL as req
from response import ResponseMySQL as res
from response import ResponseDefault as res1
from repository import ChatHistoryRepository
from repository import DetailChatRepository,UserRepository
from fastapi.responses import  JSONResponse
from function import  support_function as sf
import re
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

def check_email(email):
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False
    
async def edit_chat(request: req.RequestEditNameChat):
  try:
    user_id = request.user_id
    name_old = request.name_old
    name_new = request.name_new
    email = sf.check_email_service(user_id)
    if isinstance(email, res1.ReponseError):
        return email
    if name_old is None or name_old =="":
        return res.ReponseError(
            status=400,
            data =res.Message(message="name_old is empty")
        )
    if name_new is None or name_new == "":
        return res.ReponseError(
            status=400,
            data =res.Message(message="name_new is empty")
        )
    chat_exist = ChatHistoryRepository.getIdChatHistoryByUserIdAndNameChatNew(user_id, name_new)
    if chat_exist:
        return res.ReponseError(
            status=400,
            data=res.Message(message="name_new duplicate")
        )
    id_chat = ChatHistoryRepository.getIdChatHistoryByUserIdAndNameChat(user_id, name_old)
    if id_chat:
       ChatHistoryRepository.updateNameChatHistory(user_id,name_old,name_new)
       check = True
    else:
       check = False
    if check is True:
        return  res.ResponseEditChat(
           status= 200,
           data= res.Message(message=check)
        )
    else:
       return res.ReponseError(
            status=500,
            data =res.Message(message="Update chat error")
        )     
  except:
     return res.ReponseError(
            status=500,
            data =res.Message(message="Server Error")
        )

async def delete_chat(request: req.RequestDeleteChat):
    try:
        user_id = request.user_id
        chat_name = request.chat_name
        email = sf.check_email_service(user_id)
        if isinstance(email, res1.ReponseError):
            return email
        if chat_name is None or chat_name =="":
            return res.ReponseError(
                status=400,
                data =res.Message(message="chat_name is empty")
            )
        DetailChatRepository.delete_chat_detail(chat_name)
        chat_exist = ChatHistoryRepository.getIdChatHistoryByUserIdAndNameChat(user_id, chat_name)
        if chat_exist is None:
            return res.ReponseError(
                status=404,
                data=res.Message(message="chat_name not exist")
            )
        check = ChatHistoryRepository.deleteChatHistory(user_id,chat_name)
        if check is True:
            return  res.ResponseDeleteChat(
               status= 200,
               data= res.Message(message="Delete conversation chat success")
            )
        else:
            return res.ReponseError(
                status=500,
                data =res.Message(message="Delete conversation chat error")
            )
    except Exception as e:
        return res.ResponseDeleteChat(
            status=500,
            data=res.Message(message=str(e))
        )

async def delete_chat_detail_by_id(request: req.RequestDeleteDetailChat):
    try:
        user_id = request.user_id
        chat_detail_id = request.id_chat_detail
        email = sf.check_email_service(user_id)
        if isinstance(email, res1.ReponseError):
            return email
        if chat_detail_id is None or chat_detail_id == " ":
            return res.ReponseError(
                status=400,
                data=res.Message(message="id chat_detail is empty")
            )
        check = DetailChatRepository.delete_chat_detail_by_id((chat_detail_id))
        if check is True:
            return res.ResponseDeleteChatDetailById(
               status= 200,
               data= res.CheckModel(check=check)
            )
        else:
            return res.ResponseDeleteChatDetailById(
                status=200,
                data=res.CheckModel(check=check)
            )
    except Exception as e:
        return res.ResponseDeleteChat(
            status=500,
            data=res.Message(message=str(e))
        )

async def render_chat_history(request: req.RequestRenderChatHistory):
    try:
        user_id = request.user_id
        email = sf.check_email_service(user_id)
        if isinstance(email, res1.ReponseError):
            return email
        chat_detail = ChatHistoryRepository.getChatHistoryById(user_id)
        chat1 = [res.ListUserChat(id=item.id, email=item.email, chat_name=item.name_chat) for item in chat_detail]
        return res.ResponseRenderChatHistory(
            status=200,
            data=res.UserInfoListResponse(chat=chat1)
        )
    except Exception as e:
        return res.ReponseError(
            status=500,
            data=res.Message(message="Server Error")
        )

async def create_chat_history(request: req.RequestCreateChatHistory):
 try:
    user_id = request.user_id
    chat_name = request.chat_name
    email = sf.check_email_service(str(user_id))
    if isinstance(email, res1.ReponseError):
        return email
    if chat_name is None or chat_name == "":
        return res.ReponseError(
            status=400,
            data=res.Message(message="chat_name is empty")
        )
    check = ChatHistoryRepository.getIdChatHistoryByUserIdAndNameChat(user_id,chat_name)
    if check is not None:
        return res.ReponseError(
            status=400,
            data=res.Message(message="chat_name exist")
        )
    ChatHistoryRepository.addChatHistory(user_id,chat_name)
    return res.ResponseCreateChat(
        status=200,
        data=res.Message(message="create chat success")
    )
 except:
     return res.ReponseError(
         status=500,
         data=res.Message(message="Server Error")
     )

async def get_detail_chat_by_chat_id(request: req.RequestGetChatDetails):
      id = request.id
      if id is None or id == "":
          return res.ReponseError(
              status=400,
              data=res.Message(message="Id is empty")
          )
      chat_detail1 = DetailChatRepository.getDetailChatByChatId(id)
      if chat_detail1:
          return res.ResponseChatDetailById(
              status=200,
              data=res.ChatDetailById(
                  id = chat_detail1.id,
                  data_relevant = chat_detail1.data_relevant,
                  source_file = chat_detail1.source_file
              )
          )
      else:
          return res.ReponseError(
              status=404,
              data=res.Message(message="Chat not exist")
          )

async def load_chat_history(request: req.RequestLoadChatHistory):
  try:
    chat_id = request.chat_id
    user_id = request.user_id
    email = sf.check_email_service(str(user_id))
    if isinstance(email, res1.ReponseError):
        return email
    if chat_id is None or chat_id == "":
        return res.ReponseError(
            status = 400,
            data = res.Message(message="chat_id is empty")
        )
    check_exist_chatid_width_user_id = ChatHistoryRepository.getChatHistoryByChatIdAndUserId(chat_id,user_id)
    if check_exist_chatid_width_user_id is None:
        return res.ReponseError(
            status=404,
            data=res.Message(message="Not found chat width chat_id and user_id")
        )
    result = DetailChatRepository.getListDetailChatByChatId(chat_id)
    chat1 = [res.ChatDetail(id=item.id, chat_id = item.chat_id, question=item.YouMessage,answer=item.AiMessage,data_relevant = item.data_relevant,source_file=item.source_file) for item in result]
    return res.ResponseLoadChatHistory(
         status = 200,
         data = res.ListChatDeTail(detail_chat=chat1)
      )
  except:
      return res.ReponseError(
            status=500,
            data=res.Message(message="Server Error")
        )


async def delete_last_chat_detail_by_chat_name(request: req.RequestStopChat):
    try:
        user_id = request.user_id
        chat_name = request.chat_name
        email = sf.check_email_service(user_id)
        if isinstance(email, res1.ReponseError):
            return email
        if not chat_name:
            return res.ReponseError(
                status=400,
                data=res.Message(message="chat_name is empty")
            )
        check_exist_chat = ChatHistoryRepository.getIdChatHistoryByUserIdAndNameChat(user_id, chat_name)
        if check_exist_chat is None:
            return res.ReponseError(
                status=404,
                data=res.Message(message="Chat not exist")
            )
        check = ChatHistoryRepository.delete_last_chat_detail_by_chat_name_and_email(chat_name, user_id)
        if check:
            return res.ResponseStopChat(
                status=200,
                data=res.Message(message="stop chat success")
            )
        else:
            return res.ReponseError(
                status=500,
                data=res.Message(message="Failed to stop chat")
            )
    except Exception as e:
        return res.ReponseError(
            status=500,
            data=res.Message(message=f"Server Error: {e}")
        )