from fastapi import APIRouter, Form, Request
from service import ChatService
from request import RequestChat
from typing import Optional
from fastapi.requests import Request
from function import support_function
from response import ResponseChat as res
from fastapi import  Path,Query
router = APIRouter()

@router.post("/chatbot/query", tags=["Chat"])
async def handle_query2_upgrade_old(request: Request,
                                    user_id: str = Form(None),
                                    text_all: str = Form(...),
                                    question: Optional[str] = Form(None),
                                    chat_name: Optional[str] = Form(None)):
    check = support_function.check_value_user_id_controller(user_id)
    if check is not True:
        return check
    request = RequestChat.RequestQuery2UpgradeOld(user_id=user_id, text_all=text_all, question=question, chat_name=chat_name)
    return await ChatService.query2_upgrade_old(request)

@router.get("/chatbot/extract_file/{user_id}", tags=["Chat"])
async def extract_file(user_id: str):
    check = support_function.check_value_user_id_controller(user_id)
    if check is not True:
        return check
    request = RequestChat.RequestExtractFile(user_id=user_id)
    return await ChatService.extract_file(request)

@router.get("/chatbot/generate_question/{user_id}",tags=["Chat"])
async def generate_question(user_id: str):
    check = support_function.check_value_user_id_controller(user_id)
    if check is not True:
        return check
    request = RequestChat.RequestGenerateQuestion(user_id=user_id)
    return await ChatService.generate_question(request)