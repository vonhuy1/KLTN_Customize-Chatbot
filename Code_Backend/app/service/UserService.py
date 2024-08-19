from datetime import timedelta, datetime
from request import RequestUser as req_login
from response import ResponseUser as res_login
import requests
import json, re
from auth.authentication import signJWT
from firebase_admin import credentials, auth, exceptions
import firebase_admin
from repository import UserLoginRepository, UserRepository, UserInfoRepository, OTPRepository
import service.OTPService
from function import support_function as sf
from dotenv import load_dotenv
import os
from response import ResponseUser as res
from response import ResponseDefault as res1
load_dotenv()
CLIENT_ID_GOOGLE = os.getenv('CLIENT_ID')
API_SIGN_UP_FIREBASE_PATH = os.getenv('API_SIGN_UP_FIREBASE')
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

def get_user1(email):
    try:
        user = auth.get_user_by_email(email)
        return user
    except exceptions.FirebaseError as e:
        return None

def check_email(email):
    if isinstance(email, str) and re.fullmatch(regex, email):
        return True
    else:
        return False
from pathlib import Path
try:
 if not firebase_admin._apps:
     json_path = Path(__file__).resolve().parent / 'app' / 'firebase_certificate.json'
     cred = credentials.Certificate(str(json_path))
     fred = firebase_admin.initialize_app(cred)
except:
    if not firebase_admin._apps:
     cred = credentials.Certificate("firebase_certificate.json")
     fred = firebase_admin.initialize_app(cred)

def sign_up_with_email_and_password(email, password, username=None, return_secure_token=True):
    try:
        rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp"
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": return_secure_token
        }
        if username:
            payload["displayName"] = username 
        payload = json.dumps(payload)
        r = requests.post(rest_api_url, params={"key": API_SIGN_UP_FIREBASE_PATH}, data=payload)
        try:
            return r.json()['email']
        except Exception as e:
            pass
    except Exception as e:
        pass

def sign_in_with_email_and_password(email=None, password=None, return_secure_token=True):
    rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
    try:
        payload = {
            "returnSecureToken": return_secure_token
        }
        if email:
            payload["email"] = email
        if password:
            payload["password"] = password
        payload = json.dumps(payload)
        r = requests.post(rest_api_url, params={"key": API_SIGN_UP_FIREBASE_PATH}, data=payload)
        r.raise_for_status()
        data = r.json()
        if 'idToken' in data:
            return data['email']
        else:
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error signing in: {e}")
        return False

def update_info_user(uid, email=None, user_name=None, photo_url=None):
    user_data = {}
    if email is not None:
        user_data['email'] = email
    if user_name is not None:
        user_data['display_name'] = user_name
    if photo_url is not None and photo_url != 'N/A':
        user_data['photo_url'] = photo_url
    if user_data:
        auth.update_user(uid, **user_data)

async  def update_user_info(request: req_login.RequestUpdateUserInfo):
 try:
   email = request.email
   user_id = request.user_id
   email_check = sf.check_email_service(user_id)
   if isinstance(email_check, res1.ReponseError):
       return email_check
   check_email_fc = sf.check_email_empty_invalid(email)
   if check_email_fc is not True:
       return check_email_fc
   user = get_user1(email)
   if user: 
        user_info = UserInfoRepository.getUserInfo(user_id)
        if user_info:
          UserInfoRepository.updateUserInfo(
            request.user_id,
            request.uid,
            request.email,
            request.display_name,
            request.photo_url)
        else:
            UserInfoRepository.addUserInfo(
                request.uid,
                request.email,
                request.display_name,
                request.photo_url
            )
        update_info_user(request.uid,
            request.email,
            request.display_name,
            request.photo_url   
              )
        return res_login.ResponseUpdateUserInfo(status=200,
                data = res_login.Message(message=f"User info updated successfully"))
   else:
          return res_login.ReponseError(
            status = 404,
            data = res_login.Message(message="Not found user")
        )
 except:
     return res_login.ReponseError(
            status=500,
            data=res_login.Message(message="Server Error")
        )
 
async  def check_info_google(request: req_login.RequestCheckInfoGoogle):
 try:
   user_id = request.user_id
   check = UserRepository.getEmailUserByIdFix(user_id)
   if check is None:
       return res_login.ReponseError(
            status = 404,
            data = res_login.Message(message="user_id not exist")
        )
   email = sf.check_email_service(str(user_id))
   if isinstance(email, res.ReponseError):
       return email
   user_info = UserInfoRepository.getUserInfo(user_id)
   if user_info is not None:
       email_check = True
   else:
       email_check = False
   if email_check is not None:
    return res_login.ResponseCheckInfoGoogle(status= 200,data = res_login.CheckModel(check=email_check))
 except:
     return res_login.ReponseError(
            status=500,
            data=res_login.Message(message="Server Error")
        )
   
async def check_info_google_email(request: req_login.RequestCheckInfoGoogleEmail):
 try:
   email = request.email
   check_email_fc = sf.check_email_empty_invalid(email)
   if check_email_fc is not True:
       return check_email_fc
   user_info = UserInfoRepository.getUserInfoByEmail(email)
   if user_info is not None:
       email_check = True
   else:
       email_check = False
   if email_check is not None:
    return res_login.ResponseCheckInfoGoogle(status= 200,data = res_login.CheckModel(check=email_check))
 except:
     return res_login.ReponseError(
            status=500,
            data=res_login.Message(message="Server Error")
        )

async def check_state_login(request: req_login.RequestCheckStateLogin):
 try:
   user_id = request.user_id
   session_id_now = request.session_id_now
   email = sf.check_email_service(user_id)
   if isinstance(email, res1.ReponseError):
       return email
   elif session_id_now is None or session_id_now=="":
       return res_login.ReponseError(
            status= 400,
            data =res_login.Message(message="session_id is empty")
        )
   user = get_user1(email)
   if user:
       check1 = False
       session_id = UserLoginRepository.getUserSessionIdByUserEmail(user_id)
       print(f"session_id: {session_id}")
       if session_id != session_id_now:
         check1 = False
       else:
         check1 = True
       return res_login.ResponseCheckInfoGoogle(status= 200,data = res_login.CheckModel(check = check1))
   else:
       return res_login.ReponseError(
            status=404,
            data =res_login.Message(message="Not found user")
        )
 except:
  return res_login.ReponseError(
            status=500,
            data=res_login.Message(message="Server Error")
        )

import string, random
def generate_otp(length=6):
    characters = string.ascii_uppercase + string.digits
    otp = ''.join(random.choice(characters) for _ in range(length))
    return otp

def createOTPReset(email):
    otp = generate_otp()
    check_email_fc = sf.check_email_empty_invalid(email)
    if check_email_fc is not True:
        return check_email_fc
    OTPRepository.addOTP(email,otp)
    return otp

async def reset_password(request: req_login.RequestResetPassword):
 try:
    email = request.email
    check_email_fc = sf.check_email_empty_invalid(email)
    if check_email_fc is not True:
        return check_email_fc
    try:
       user = get_user1(email)
       if user is not None:
           otp = createOTPReset(email)
           return res_login.ResponseCreateOTP(
               status= 200,
               data= res_login.CheckModel(check = True),
               otp = otp
           )
       else:
           return res_login.ReponseError(
               status= 404,
               data =res_login.Message(message="Email not exist")
           )
    except auth.UserNotFoundError as e:
           return res_login.ReponseError(
            status=500,
            data =res_login.Message(message=str(e))
        )
 except:
     return res_login.ReponseError(
            status=500,
            data=res_login.Message(message="Server Error")
        )

async def change_password(request: req_login.RequestChangePassword):
 try:
    user_id = request.user_id
    email = sf.check_email_service(user_id)
    new_password = request.new_password
    current_password= request.current_password
    confirm_new_password = request.confirm_new_password
    if isinstance(email, res1.ReponseError):
        return email
    if new_password is None:
        return res_login.ReponseError(
            status=400,
            data =res_login.Message(message="new_password is empty")
        )
    if current_password is None or confirm_new_password == "":
        return res_login.ReponseError(
            status=400,
            data =res_login.Message(message="current_password is empty")
        )
    if confirm_new_password is None or confirm_new_password == "":
        return res_login.ReponseError(
            status=400,
            data =res_login.Message(message="confirm_new_password is empty")
        )
    if current_password == new_password:
        return res_login.ReponseError(
            status=400,
            data=res_login.Message(message="The new_password and the current_password must be different")
        )
    if confirm_new_password != new_password:
        return res_login.ReponseError(
            status=400,
            data=res_login.Message(message="The new_password and the confirm_new_password must be similar")
        )
    user = sign_in_with_email_and_password(email, current_password)
    try:
     if user:
      user_email = auth.get_user_by_email(email)
      auth.update_user(
        user_email.uid,
        password=new_password
    ) 
      return res_login.ResponseChangePassword(
               status= 200,
               data = res_login.Message(message=f"Update password success"))
     else:
        return res_login.ReponseError(
            status=400,
            data =res_login.Message(message="Current password not valid")
        )
    except :
      return res_login.ReponseError(
            status=500,
            data =res_login.Message(message="Server Error")
        )
 except:
     return res_login.ReponseError(
            status=500,
            data=res_login.Message(message="Server Error!!")
        )