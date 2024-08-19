from typing import Union
from datetime import timedelta
from request import RequestChat as req
from response import ResponseChat as res
from repository import ChatHistoryRepository, DetailChatRepository, UserRepository
import function.chatbot as sf
from typing import Dict
import json, re
from pydantic import BaseModel
from function import support_function
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

def check_email(email):
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

class Document(BaseModel):
    page_content: str
    metadata: Dict[str, str]
    type: str

async def query2_upgrade_old(request: req.RequestQuery2UpgradeOld):
  try:
    user_id = request.user_id
    question = request.question
    text_all = request.text_all
    chat_name = request.chat_name
    email = support_function.check_email_service(str(user_id))
    if isinstance(email, res.ReponseError):
        return email
    if question is None:
        return res.ReponseError(
            status=400,
            data =res.Message(message="question is empty")
        )
    if chat_name is None:
        return res.ReponseError(
            status=400,
            data =res.Message(message="chat_name is empty")
        )
    text_all_dicts = json.loads(text_all)
    text_all1 = [Document(**doc) for doc in text_all_dicts]
    chat_id_exist = ChatHistoryRepository.getIdChatHistoryByUserIdAndNameChat(user_id, chat_name)
    chat_history = ""
    if chat_id_exist:
        list_chat_detail = DetailChatRepository.getListDetailChatByChatId(chat_id_exist)
        for item in list_chat_detail:
            chat_history += f"You: {item.YouMessage}\nAI: {item.AiMessage}\n\n"

    test, list1, list2 = sf.handle_query_upgrade_keyword_old(question, text_all1, email,chat_history)
    text1 = "<Data_Relevant>".join(list1)
    text2 = "<Source_File>".join(list2)
    id = 0
    if test:
       chat_id = ChatHistoryRepository.getIdChatHistoryByUserIdAndNameChat(user_id,chat_name)
       if chat_id:
           id = DetailChatRepository.addDetailChat(chat_id,question, test, text1, text2)
       if chat_id is None:
           ChatHistoryRepository.addChatHistory(user_id,chat_name)
           chat_id_new = ChatHistoryRepository.getIdChatHistoryByUserIdAndNameChat(user_id,chat_name)
           id = DetailChatRepository.addDetailChat(chat_id_new, question, test, text1, text2)
       return res.ResponseQuery2UpgradeOld(
               status= 200,
               data = res.DataAnswer1(id = id,
                                      answer=test,
                                      data_relevant=list1,
                                      sources=list2))
    if test is None or test == "":
         return res.ReponseError(
            status=500,
            data =res.Message(message="No answer")
        )
  except:
     return res.ReponseError(
            status=500,
            data =res.Message(message="Server Error")
        )

async def extract_file(request: req.RequestExtractFile):
 try:
   user_id = request.user_id
   email = support_function.check_email_service(str(user_id))
   if isinstance(email, res.ReponseError):
       return email
   text_all1 = sf.extract_data2(email)
   if text_all1 is False:
       return res.ResponseExtractFile(
               status= 200,
               data = res.DataExtractFile(text_all="No data response"))
   return res.ResponseExtractFile(
               status= 200,
               data = res.DataExtractFile(text_all=text_all1))
 except:
     return res.ReponseError(
            status=500,
            data =res.Message(message="Server Error")
        )

async def generate_question(request: req.RequestGenerateQuestion):
 try:
   user_id = request.user_id
   email = support_function.check_email_service(str(user_id))
   if isinstance(email, res.ReponseError):
       return email
   text_all1 = sf.generate_question(email)
   if text_all1 is False:
       return res.ResponseGenerateQuestion(
               status= 200,
               data = res.GenerateQuestion(question=False))
     
   return res.ResponseGenerateQuestion(
               status= 200,
               data = res.GenerateQuestion(question=text_all1))
 except:
     return res.ReponseError(
            status=500,
            data=res.Message(message="Server Error")
        )

async def delete_chat(request: req.RequestDeleteChat):
  try:
    user_id = request.user_id
    email = support_function.check_email_service(str(user_id))
    if isinstance(email, res.ReponseError):
        return email
    chat_name = request.chat_name
    if chat_name is None:
        return res.ReponseError(
            status=400,
            data =res.Message(message="chat_name is empty")
        )
    DetailChatRepository.delete_chat_detail(chat_name)
    check = ChatHistoryRepository.deleteChatHistory(user_id,chat_name)
    if check is False:
       return res.ResponseDeleteChat(
               status = 500,
               data = res.Message(message="Delete conversation chat failed"))
    else:
       return res.ResponseDeleteChat(
               status = 200,
               data = res.Message(message="Delete conversation chat success"))
  except:
     return res.ReponseError(
            status= 500,
            data = res.Message(message="Server Error")
        )