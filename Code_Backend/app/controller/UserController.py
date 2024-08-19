from fastapi import APIRouter, Query
from request import RequestUser
from response import ResponseUser as res
from service import UserService
from function import support_function
from fastapi import HTTPException
from response import ResponseUser as res
router = APIRouter()

@router.put("/update_user_info", tags=["User"])
async def update_user_info(request: RequestUser.RequestUpdateUserInfo):
    user_id = request.user_id
    check = support_function.check_value_user_id_controller(user_id)
    if check is not True:
        return check
    uid = request.uid
    email = request.email
    display_name = request.display_name
    photo_url = request.photo_url
    if uid is None or uid.strip() == "":
        return res.ReponseError(status=400,
                                data=res.Message(message="uid field is required.")) 
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

@router.get('/check_info_google', tags=["User"])
async def check_info_google(user_id: str = Query(None)):
    check = support_function.check_value_user_id_controller(user_id)
    if check is not True:
        return check
    request =RequestUser.RequestCheckInfoGoogle(user_id=user_id)
    return await UserService.check_info_google(request)

@router.get('/check_info_google_signup', tags=["User"])
async def check_info_google_signup(email: str = None):
    check = support_function.check_value_email_controller(email)
    if check is not True:
        return check
    request =RequestUser.RequestCheckInfoGoogleEmail(email=email)
    return await UserService.check_info_google_email(request)

@router.get('/check_state_login', tags=["User"])
async def check_state_login(user_id: str = Query(None), session_id_now: str = Query(None)):
    check = support_function.check_value_user_id_controller(user_id)
    if check is not True:
        return check
    if session_id_now is None or session_id_now.strip() == "":
        return res.ReponseError(status=400,
                                data=res.Message(message="Session Id is required."))
    try:
        int(session_id_now)
        return res.ReponseError(status=400,
                                data=res.Message(message="Session Id must be a string, not a number."))
    except ValueError:
        pass
    request =RequestUser.RequestCheckStateLogin(user_id=user_id, session_id_now=session_id_now)
    return await UserService.check_state_login(request)


@router.post('/reset_password', tags=["User"])
async def reset_password(request:RequestUser.RequestResetPassword):
    email = request.email
    check = support_function.check_value_email_controller(email)
    if check is not True:
        return check
    return await UserService.reset_password(request)

@router.put('/change_password', tags=["User"])
async def reset_password_firebase(request:RequestUser.RequestChangePassword):
    user_id = request.user_id
    check = support_function.check_value_user_id_controller(user_id)
    if check is not True:
        return check
    new_password = request.new_password
    current_password = request.current_password
    confirm_new_password = request.confirm_new_password
    if confirm_new_password is None or confirm_new_password.strip() == "":
        return res.ReponseError(status=400,
                                data=res.Message(message="Confirm New password field is required."))
    elif new_password is None or new_password.strip() == "":
        return res.ReponseError(status=400,
                                data=res.Message(message="New password field is required."))
    elif current_password is None or current_password.strip() == "":
        return res.ReponseError(status=400,
                                data=res.Message(message="Current password field is required."))
    return await UserService.change_password(request)