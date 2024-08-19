from fastapi import HTTPException, Depends, Query,APIRouter
from service import DefaultService
from request import RequestDefault
from request import RequestDefault as req
from function import support_function
from auth.authentication import decodeJWT
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from auth import authentication
from fastapi.requests import Request
from response import ResponseDefault as res
from fastapi import  File, UploadFile, Form
router = APIRouter()

@router.get("/is_me", tags=["Default"])
async def is_me(token: str = Query(...)):
    if token.strip() == "" or token is None:
        return res.ReponseError(status=400,
                                data=res.Message(message="Token field is required."))
    if token.lower() == "none":
        return res.ReponseError(status=400,
                                data=res.Message(message="Token cannot be None."))
    if not isinstance(token, str):
        return res.ReponseError(status=400,
                                data=res.Message(message="Token must be a non-empty string."))
    try:
        float(token)
        return res.ReponseError(status=400,
                                data=res.Message(message="Token must be a string, not a number."))
    except ValueError:
        pass
    request = RequestDefault.RequestIsMe(token=token)
    return await DefaultService.is_me(request)

@router.post('/create_firebase_user_google', tags=["Default"])
async def get_or_create_firebase_user(request: RequestDefault.RequestCreateFireBaseUserGoogle):
    email = request.email
    check = support_function.check_value_email_controller(request.email)
    if check is not True:
        return check
    token_google = request.token_google
    if token_google == "" or token_google is None:
        return res.ReponseError(status=400,
                                data=res.Message(message="Token field is required."))
    if not isinstance(token_google, str):
        return res.ReponseError(status=400,
                                data=res.Message(message="Token must be a non-empty string."))
    try:
        float(token_google)
        return res.ReponseError(status=400,
                                data=res.Message(message="Token must be a string, not a number."))
    except ValueError:
        pass
    return await DefaultService.create_firebase_user(request)

@router.get("/info_user/{user_id}", tags=["Default"])
async def get_user(user_id: str):
    check = support_function.check_value_user_id_controller(user_id)
    if check is not True:
        return check
    request = RequestDefault.RequestInfoUser(user_id=user_id)
    return await DefaultService.info_user(request)

ALLOWED_IMAGE_EXTENSIONS = {"jpeg", "jpg", "png"}

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

@router.post("/upload_image", tags=["Default"])
async def upload_image(user_id: str = Form(None), file: UploadFile = File(...)):
    check = support_function.check_value_user_id_controller(user_id)
    if check is not True:
        return check
    request = req.RequestUpLoadImage(user_id=user_id, files= file)
    return await DefaultService.upload_image_service(request)