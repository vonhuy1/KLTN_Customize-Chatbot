from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from controller import UserController, FileController, MySQLController, DefaultController, OTPController,AuthenticationController
import firebase_admin
from controller import ChatController
from firebase_admin import credentials
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from service import MySQLService, UserService, ChatService
from request import RequestMySQL, RequestUser, RequestDefault
from auth.authentication import decodeJWT
from repository import UserRepository
from auth import authentication
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, Form, File, UploadFile
from typing import List
from service import FileService, DefaultService, UserService,AuthService
from request import RequestFile, RequestChat, RequestDefault
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic.error_wrappers import ErrorWrapper
from fastapi import Query
from typing import Optional
import json
from function import support_function
from response import ResponseDefault as res
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
app = FastAPI(
    title="ChatBot HCMUTE",
    description="Python ChatBot is intended for use in the topic Customizing chatbots. With the construction of 2 students Vo Nhu Y - 20133118 and Nguyen Quang Phuc 20133080",
    swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
    version="1.0.0",
    contact={
        "name": "Vo Nhu Y",
        "url": "https://pychatbot1.streamlit.app",
        "email": "vonhuy5112002@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }
)
origins = [
    "http://localhost:9090",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
ALLOWED_EXTENSIONS = {'csv', 'txt', 'doc', 'docx', 'pdf', 'xlsx', 'pptx', 'json', 'md'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_certificate.json")
    fred = firebase_admin.initialize_app(cred)

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(status_code=401, detail="Invalid authentication scheme.")
            if not self.verify_accesstoken(credentials.credentials):
                raise HTTPException(status_code=401, detail="Token does not exist")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=401, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=401, detail="Invalid authorization code.")

    def verify_accesstoken(self, jwtoken: str) -> bool:
        check = AuthService.check_token_is_valid(jwtoken)
        return check

    def verify_jwt(self, jwtoken: str) -> bool:
        try:
            payload = decodeJWT(jwtoken)
            email_encode = payload.get('sub')
            self.email = authentication.str_decode(email_encode)
            return True
        except Exception as e:
            print(e)
            return False

def get_current_user_email(credentials: str = Depends(JWTBearer())):
    try:
        payload = decodeJWT(credentials)
        email_encode = payload.get('sub')
        email = authentication.str_decode(email_encode)
        return email
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="Invalid token or expired token.")


@app.get("/api/v1/mysql/chat_history/{user_id}", dependencies=[Depends(JWTBearer())], tags=["MySQL"])
async def override_render_chat(user_id: str,
                               current_user_email: str = Depends(get_current_user_email)):
    check = support_function.check_value_user_id(user_id, current_user_email)
    if check is not True:
        return check
    request = RequestMySQL.RequestRenderChatHistory(user_id=user_id)
    return await MySQLService.render_chat_history(request)

@app.delete("/api/v1/mysql/chat_history/delete_last_chat_record",dependencies=[Depends(JWTBearer())], tags=["MySQL"])
async def override_delete_last_chat_record(request: RequestMySQL.RequestStopChat, current_user_email: str = Depends(get_current_user_email)):
    user_id = request.user_id
    check = support_function.check_value_user_id_controller(user_id)
    if check is not True:
        return check
    chat_name = request.chat_name
    if chat_name is None or chat_name.strip() == "":
        raise HTTPException(status_code=400, detail="chat_name field is required.")
    return await MySQLService.delete_last_chat_detail_by_chat_name(request)

@app.post("/api/v1/mysql/chat_history/create", dependencies=[Depends(JWTBearer())], tags=["MySQL"])
async def override_create_chat_history(request:RequestMySQL.RequestCreateChatHistory,current_user_email: str = Depends(get_current_user_email)):
    check = support_function.check_value_user_id(request.user_id, current_user_email)
    if check is not True:
        return check
    chat_name = request.chat_name
    if chat_name is None or chat_name.strip() == "":
        raise HTTPException(status_code=400, detail="chat_name field is required.")
    return await MySQLService.create_chat_history(request)

@app.put("/api/v1/mysql/edit_chat", dependencies=[Depends(JWTBearer())], tags=["MySQL"])
async def override_edit_chat(request: RequestMySQL.RequestEditNameChat,
                             current_user_email: str = Depends(get_current_user_email)):
    user_id = request.user_id
    check = support_function.check_value_user_id(user_id, current_user_email)
    if check is not True:
        return check
    name_new = request.name_new
    if name_new is None or name_new.strip() == "":
        raise HTTPException(status_code=400, detail="name_new field is required.")
    name_old = request.name_old
    if name_old is None or name_old.strip() == "":
        raise HTTPException(status_code=400, detail="name_old field is required.")
    return await MySQLService.edit_chat(request)

@app.delete("/api/v1/mysql/chat_history/delete", dependencies=[Depends(JWTBearer())], tags=["MySQL"])
async def override_delete_chat(request: RequestMySQL.RequestDeleteChat,
                               current_user_email: str = Depends(get_current_user_email)):
    user_id = request.user_id
    check = support_function.check_value_user_id(user_id, current_user_email)
    if check is not True:
        return check
    chat_name = request.chat_name
    if chat_name is None or chat_name.strip() == "":
        raise HTTPException(status_code=400, detail="chat_name field is required.")
    return await MySQLService.delete_chat(request)

@app.delete("/api/v1/mysql/detail_chat/delete", dependencies=[Depends(JWTBearer())], tags=["MySQL"])
async def override_delete_detail_chat_detail(request: RequestMySQL.RequestDeleteDetailChat,
                               current_user_email: str = Depends(get_current_user_email)):
    user_id = request.user_id
    check = support_function.check_value_user_id(user_id, current_user_email)
    if check is not True:
        return check
    id_chat_detail = request.id_chat_detail
    if id_chat_detail is None or id_chat_detail.strip() == "":
        raise HTTPException(status_code=400, detail="id_chat_detail field is required.")
    return await MySQLService.delete_chat_detail_by_id(request)

@app.get("/api/v1/mysql/detail_chat/{user_id}/{chat_id}", dependencies=[Depends(JWTBearer())], tags=["MySQL"])
async def override_load_chat(chat_id: str, user_id: str,
                             current_user_email: str = Depends(get_current_user_email)):
    check = support_function.check_value_user_id(user_id, current_user_email)
    if check is not True:
        return check
    if chat_id is None or chat_id.strip() == "":
        return res.ReponseError(status=400,
                                data=res.Message(message="chat_id field is required."))
    chat_id = chat_id.strip("'").strip('"')
    try:
        chat_id_int = int(chat_id)
    except ValueError:
        return res.ReponseError(status=400,
                                data=res.Message(message="chat_id must be an integer"))
    if not support_function.is_positive_integer(chat_id_int):
        return res.ReponseError(status=400,
                                data=res.Message(message="chat_id must be greater than 0"))
    request = RequestMySQL.RequestLoadChatHistory(chat_id=chat_id, user_id=user_id)
    return await MySQLService.load_chat_history(request)


@app.get("/api/v1/default/info_user/{user_id}", dependencies=[Depends(JWTBearer())], tags=["Default"])
async def override_get_user(user_id: str , current_user_email: str = Depends(get_current_user_email)):
    check = support_function.check_value_user_id(user_id, current_user_email)
    if check is not True:
        return check
    request = RequestDefault.RequestInfoUser(user_id=user_id)
    return await DefaultService.info_user(request)


@app.put("/api/v1/users/update_user_info", dependencies=[Depends(JWTBearer())], tags=["User"])
async def override_update_user_info(request: RequestUser.RequestUpdateUserInfo,
                                    current_user_email: str = Depends(get_current_user_email)):
    user_id = request.user_id
    check = support_function.check_value_user_id(user_id, current_user_email)
    if check != True:
        return check
    uid = request.uid
    email = request.email
    display_name = request.display_name
    photo_url = request.photo_url
    if uid is None or uid.strip() == "":
        raise HTTPException(status_code=400, detail="uid field is required.")
    if email is None or email.strip() == "":
        return res.ReponseError(status=400,
                                data=res.Message(message="email field is required."))
    if display_name is None or display_name.strip() == "":
        return res.ReponseError(status=400,
                                data=res.Message(message="display_name field is required."))
    if photo_url is None or photo_url.strip() == "":
        return res.ReponseError(status=400,
                                data=res.Message(message="photo_url field is required."))
    return await UserService.update_user_info(request)

@app.put('/api/v1/users/change_password', dependencies=[Depends(JWTBearer())], tags=["User"])
async def override_reset_password_firebase(request: RequestUser.RequestChangePassword,
                                           current_user_email: str = Depends(get_current_user_email)):
    user_id = request.user_id
    check = support_function.check_value_user_id(user_id, current_user_email)
    if check != True:
        return check
    new_password = request.new_password
    current_password = request.current_password
    confirm_new_password = request.confirm_new_password

    if new_password is None or new_password.strip() == "":
        return res.ReponseError(status=400,
                                data=res.Message(message="new_password field is required."))
    if current_password is None or current_password.strip() == "":
        return res.ReponseError(status=400,
                                data=res.Message(message="current_password field is required."))
    if confirm_new_password is None or confirm_new_password.strip() == "":
        return res.ReponseError(status=400,
                                data=res.Message(message="confirm_new_password field is required."))

    return await UserService.change_password(request)

@app.delete("/api/v1/file/delete", dependencies=[Depends(JWTBearer())], tags=["File"])
async def override_delete_folder(request: RequestFile.RequestDeleteAllFile,
                                 current_user_email: str = Depends(get_current_user_email)):
    check = support_function.check_value_user_id(request.user_id, current_user_email)
    if check != True:
        return check
    return await FileService.deleteAllFile(request)

@app.delete("/api/v1/file/delete_file", dependencies=[Depends(JWTBearer())], tags=["File"])
async def override_delete_one_file(request: RequestFile.RequestDeleteFile,
                                   current_user_email: str = Depends(get_current_user_email)):
    user_id = request.user_id
    check = support_function.check_value_user_id(user_id, current_user_email)
    if check != True:
        return check
    name_file = request.name_file
    if name_file is None or name_file.strip() == "":
        return res.ReponseError(status=400,
                                data=res.Message(message="name_file is required."))
    return await FileService.deleteFile(request)

@app.post("/api/v1/file/chatbot/download_folder", dependencies=[Depends(JWTBearer())], tags=["File"])
async def override_download_folder_from_dropbox(request: RequestFile.RequestDownLoadFolder,
                                                current_user_email: str = Depends(get_current_user_email)):
    user_id = request.user_id
    check = support_function.check_value_user_id(user_id, current_user_email)
    if check is not True:
        return check
    return await FileService.download_folder(request)

@app.post("/api/v1/file/chatbot/download_files", dependencies=[Depends(JWTBearer())], tags=["File"])
async def override_download_file_by_id(request: RequestFile.RequestDownLoadFile,
                                       current_user_email: str = Depends(get_current_user_email)):
    user_id = request.user_id
    check = support_function.check_value_user_id(user_id, current_user_email)
    if check is not True:
        return check
    return await  FileService.download_file(request)

@app.post("/api/v1/file/upload_files", dependencies=[Depends(JWTBearer())], tags=["File"])
async def override_upload_files_dropbox(
        user_id: str = Form(None),
        files: List[UploadFile] = File(None),
        current_user_email: str = Depends(get_current_user_email)
):
    check = support_function.check_value_user_id(user_id, current_user_email)
    if check is not True:
        return check
    for file in files:
        if file.size > 15 * 1024 * 1024:
            raise HTTPException(status_code=413,
                                detail=f"File {file.filename} too large. Maximum size allowed is 15MB.")
    request = RequestFile.RequestUploadFile(files=files, user_id=user_id)
    return await FileService.upload_files(request)

@app.post("/api/v1/chat/chatbot/query", dependencies=[Depends(JWTBearer())], tags=["Chatbot"])
async def override_handle_query2_upgrade_old(request: Request, user_id: str = Form(None), text_all: str = Form(...),
                                             question: str = Form(None), chat_name: str = Form(None),
                                             current_user_email: str = Depends(get_current_user_email)):
    check = support_function.check_value_user_id(user_id, current_user_email)
    if check is not True:
        return check
    request = RequestChat.RequestQuery2UpgradeOld(user_id=user_id, text_all=text_all, question=question,
                                                  chat_name=chat_name)
    return await ChatService.query2_upgrade_old(request)

@app.get("/api/v1/chat/chatbot/extract_file/{user_id}", dependencies=[Depends(JWTBearer())], tags=["Chatbot"])
async def override_extract_file(user_id: str, current_user_email: str = Depends(get_current_user_email)):
    check = support_function.check_value_user_id(user_id, current_user_email)
    if check is not True:
        return check
    request = RequestChat.RequestExtractFile(user_id=user_id)
    return await ChatService.extract_file(request)

@app.get("/api/v1/chat/chatbot/generate_question/{user_id}", dependencies=[Depends(JWTBearer())], tags=["Chatbot"])
async def override_generate_question(user_id: str, current_user_email: str = Depends(get_current_user_email)):
    check = support_function.check_value_user_id(user_id, current_user_email)
    if check is not True:
        return check
    request = RequestChat.RequestGenerateQuestion(user_id=user_id)
    return await ChatService.generate_question(request)

@app.post("/api/v1/default/upload_image", dependencies=[Depends(JWTBearer())], tags=["Default"])
async def override_upload_image(user_id: str = Form(None), file: UploadFile = File(...),
                                current_user_email: str = Depends(get_current_user_email)):
    if file.file.size > 10 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File too large")
    check = support_function.check_value_user_id(user_id, current_user_email)
    if check is not True:
        return check
    request = RequestDefault.RequestUpLoadImage(user_id=user_id, files=file)
    return await DefaultService.upload_image_service(request)

app.include_router(AuthenticationController.router, tags=["Authentication"], prefix="/api/v1/auth")
app.include_router(MySQLController.router, prefix="/api/v1/mysql")
app.include_router(UserController.router, prefix="/api/v1/users")
app.include_router(FileController.router, prefix="/api/v1/file")
app.include_router(ChatController.router, prefix="/api/v1/chat")
app.include_router(DefaultController.router, prefix="/api/v1/default")

routes_to_override = {
    "/api/v1/mysql/chat_history/{user_id}": {"GET"},
    "/api/v1/mysql/detail_chat/{user_id}/{chat_id}": {"GET"},
    "/api/v1/mysql/edit_chat": {"PUT"},
    "/api/v1/mysql/chat_history/delete": {"DELETE"},
    "/api/v1/users/update_user_info": {"PUT"},
    "/api/v1/users/change_password": {"PUT"},
    "/api/v1/file/delete": {"DELETE"},
    "/api/v1/file/delete_file": {"DELETE"},
    "/api/v1/file/chatbot/download_folder": {"POST"},
    "/api/v1/file/chatbot/download_files": {"POST"},
    "/api/v1/file/upload_files": {"POST"},
    "/api/v1/chat/chatbot/query": {"POST"},
    "/api/v1/chat/chatbot/extract_file/{user_id}": {"GET"},
    "/api/v1/chat/chatbot/generate_question/{user_id}": {"GET"},
    "/api/v1/default/upload_image": {"POST"},
    "/api/v1/default/info_user/{user_id}": {"GET"},
    "/api/v1/mysql/detail_chat/delete":{"DELETE"},
    "/api/v1/mysql/chat_history/create": {"POST"},
    "/api/v1/mysql/chat_history/delete_last_chat_record": {"DELETE"}
}

app.router.routes = [
    route for route in app.router.routes
    if not (
            route.path in routes_to_override and
            route.methods.intersection(routes_to_override[route.path])
    )
]

app.add_api_route("/api/v1/mysql/chat_history/{user_id}", override_render_chat, methods=["GET"],
                  dependencies=[Depends(JWTBearer())], tags=["MySQL"])
app.add_api_route("/api/v1/mysql/detail_chat/{user_id}/{chat_id}", override_load_chat, methods=["GET"],
                  dependencies=[Depends(JWTBearer())], tags=["MySQL"])
app.add_api_route("/api/v1/mysql/edit_chat", override_edit_chat, methods=["PUT"], dependencies=[Depends(JWTBearer())],
                  tags=["MySQL"])
app.add_api_route("/api/v1/mysql/chat_history/create", override_create_chat_history, methods=["POST"], dependencies=[Depends(JWTBearer())],
                  tags=["MySQL"])
app.add_api_route("/api/v1/mysql/chat_history/delete", override_delete_chat, methods=["DELETE"],
                  dependencies=[Depends(JWTBearer())], tags=["MySQL"])
app.add_api_route("/api/v1/mysql/chat_history/delete_last_chat_record", override_delete_last_chat_record, methods=["DELETE"],
                  dependencies=[Depends(JWTBearer())], tags=["MySQL"])
app.add_api_route("/api/v1/mysql/detail_chat/delete", override_delete_detail_chat_detail, methods=["DELETE"],
                  dependencies=[Depends(JWTBearer())], tags=["MySQL"])
app.add_api_route("/api/v1/users/update_user_info", override_update_user_info, methods=["PUT"],
                  dependencies=[Depends(JWTBearer())], tags=["User"])
app.add_api_route("/api/v1/users/change_password", override_reset_password_firebase, methods=["PUT"],
                  dependencies=[Depends(JWTBearer())], tags=["User"])
app.add_api_route("/api/v1/file/delete", override_delete_folder, methods=["DELETE"],
                  dependencies=[Depends(JWTBearer())], tags=["File"])
app.add_api_route("/api/v1/file/delete_file", override_delete_one_file, methods=["DELETE"],
                  dependencies=[Depends(JWTBearer())], tags=["File"])
app.add_api_route("/api/v1/file/chatbot/download_folder", override_download_folder_from_dropbox, methods=["POST"],
                  dependencies=[Depends(JWTBearer())], tags=["File"])
app.add_api_route("/api/v1/file/chatbot/download_files", override_download_file_by_id, methods=["POST"],
                  dependencies=[Depends(JWTBearer())], tags=["File"])
app.add_api_route("/api/v1/file/upload_files", override_upload_files_dropbox, methods=["POST"],
                  dependencies=[Depends(JWTBearer())], tags=["File"])
app.add_api_route("/api/v1/chat/chatbot/query", override_handle_query2_upgrade_old, methods=["POST"],
                  dependencies=[Depends(JWTBearer())], tags=["Chat"])
app.add_api_route("/api/v1/chat/chatbot/extract_file/{user_id}", override_extract_file, methods=["GET"],
                  dependencies=[Depends(JWTBearer())], tags=["Chat"])
app.add_api_route("/api/v1/chat/chatbot/generate_question/{user_id}", override_generate_question, methods=["GET"],
                  dependencies=[Depends(JWTBearer())], tags=["Chat"])
app.add_api_route("/api/v1/default/upload_image", override_upload_image, methods=["POST"],
                  dependencies=[Depends(JWTBearer())], tags=["Default"])
app.add_api_route("/api/v1/default/info_user/{user_id}", override_get_user, methods=["GET"], dependencies=[Depends(JWTBearer())],
                  tags=["Default"])
app.include_router(OTPController.router, tags=["OTP"], prefix="/api/v1/otp")
import nest_asyncio
from uvicorn import run
nest_asyncio.apply()
import os

if __name__ == "__main__":
    run(app, port=9090)