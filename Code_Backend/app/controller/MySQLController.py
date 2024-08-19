from fastapi import Query, APIRouter
from service import MySQLService
from request import RequestMySQL
from response import ResponseMySQL as res
from typing import Optional
from request import RequestMySQL as req
from function import support_function
from fastapi import HTTPException
router = APIRouter()

@router.get("/chat_history/{user_id}", tags=["MySQL"])
async def render_chat(user_id: str):
    check = support_function.check_value_user_id_controller(user_id)
    if check is not True:
        return check
    request = RequestMySQL.RequestRenderChatHistory(user_id=user_id)
    return await MySQLService.render_chat_history(request)

@router.get("/data_relevant/{detail_chat_id}", tags=["MySQL"])
async def render_chat_1(detail_chat_id: str):
    if detail_chat_id is None or detail_chat_id.strip() == "":
        return res.ReponseError(status=400,
                                data=res.Message(message="Id field is required."))
    detail_chat_id = detail_chat_id.strip("'").strip('"')
    try:
        detail_chat_id_int = int(detail_chat_id)
    except ValueError:
        return res.ReponseError(status=400,
                                data=res.Message(message="Value must be an integer"))
    if not support_function.is_positive_integer(detail_chat_id_int):
        return res.ReponseError(status=400,
                                data=res.Message(message="Value must be greater than 0"))
    request = req.RequestGetChatDetails(id=detail_chat_id)
    return await MySQLService.get_detail_chat_by_chat_id(request)

@router.get("/detail_chat/{user_id}/{chat_id}", tags=["MySQL"])
async def load_chat(chat_id: str, user_id: str):
    check = support_function.check_value_user_id_controller(user_id)
    if check is not True:
        return check
    if chat_id is None or chat_id.strip() == "":
        return res.ReponseError(status=400,
                                data=res.Message(message="Chat id field is required."))
    chat_id = chat_id.strip("'").strip('"')
    try:
        chat_id_int = int(chat_id)
    except ValueError:
        return res.ReponseError(status=400,
                                data=res.Message(message="Value must be an integer"))
    if not support_function.is_positive_integer(chat_id_int):
        return res.ReponseError(status=400,
                                data=res.Message(message="Value must be greater than 0"))
    request = req.RequestLoadChatHistory(chat_id=chat_id,user_id = user_id)
    return await MySQLService.load_chat_history(request)

@router.put("/edit_chat",  tags=["MySQL"])
async def edit_chat(request: RequestMySQL.RequestEditNameChat):
    user_id = request.user_id
    check = support_function.check_value_user_id_controller(user_id)
    if check is not True:
        return check
    return await MySQLService.edit_chat(request)

@router.delete("/chat_history/delete",  tags=["MySQL"])
async def delete_chat(request: RequestMySQL.RequestDeleteChat):
    user_id = request.user_id
    check = support_function.check_value_user_id_controller(user_id)
    if check is not True:
        return check
    return await MySQLService.delete_chat(request)

@router.delete("/detail_chat/delete",  tags=["MySQL"])
async def delete_chat_detail(request: RequestMySQL.RequestDeleteDetailChat):
    user_id = request.user_id
    check = support_function.check_value_user_id_controller(user_id)
    if check is not True:
        return check
    return await MySQLService.delete_chat_detail_by_id(request)

@router.post("/chat_history/create", tags=["MySQL"])
async def create_chat_history(request: RequestMySQL.RequestCreateChatHistory):
    user_id = request.user_id
    check = support_function.check_value_user_id_controller(user_id)
    if check is not True:
        return check
    return await MySQLService.create_chat_history(request)

@router.delete("/chat_history/delete_last_chat_record", tags=["MySQL"])
async def delete_last_chat_record(request: RequestMySQL.RequestStopChat):
    user_id = request.user_id
    check = support_function.check_value_user_id_controller(user_id)
    if check is not True:
        return check
    return await MySQLService.delete_last_chat_detail_by_chat_name(request)