from fastapi import APIRouter, Query
from request import RequestAuth
from response import ResponseAuth as res
from service import AuthService
from function import support_function
from fastapi import HTTPException
router = APIRouter()

@router.post('/login', tags=["Authentication"])
async def login(request: RequestAuth.RequestLoginEmail):
    email = request.email
    check = support_function.check_value_email_controller(email)
    if check is not True:
        return check
    password = request.password
    if password is None or password.strip() == "":
        return res.ReponseError(status=400,
                                data=res.Message(message="Password is required."))
    return await AuthService.login(request)

@router.post('/login_google', tags=["Authentication"])
async def login_google(request: RequestAuth.RequestLoginGoogle):
    email = request.email
    token_google = request.token_google
    check = support_function.check_value_email_controller(email)
    if check is not True:
        return check
    if token_google is None or token_google.strip() == "":
        return res.ReponseError(status=400,
                                data=res.Message(message="token_google oauth2 is required."))
    if token_google.isdigit():
        return res.ReponseError(status=400,
                                data=res.Message(message="token_google must be a string, not a number."))
    return await AuthService.login_google(request)

@router.post('/sign_up', tags=["Authentication"])
async def signup(request: RequestAuth.RequestRegister):
    email = request.email
    check = support_function.check_value_email_controller(email)
    if check is not True:
        return check
    password = request.password
    confirm_password = request.confirm_password
    if password is None or password.strip( )== "":
        return res.ReponseError(status=400,
                                data=res.Message(message="Password is required."))
    if confirm_password is None or confirm_password.strip() == "":
        return res.ReponseError(status=400,
                                data=res.Message(message="Confirm Password is required."))
    return await AuthService.sign_up(request)


@router.post('/refresh_token', tags=["Authentication"])
async def refresh_token_account(request: RequestAuth.RequestRefreshTokenLogin):
    token = request.refresh_token
    if token is None or token.strip() == "":
        return res.ReponseError(status=400,
                                data=res.Message(message="token is required."))
    elif token.isdigit():
        return res.ReponseError(status=400,
                                data=res.Message(message="token must be string"))

    return await AuthService.refresh_token(request)