from datetime import timedelta, datetime
from request import RequestAuth as req
from response import ResponseAuth as res
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
            if r.status_code == 200:
                response_data = r.json()
                email = response_data.get('email')
                display_name = response_data.get('displayName')  # Lấy displayName nếu có
                return email, display_name
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


async def login(request: req.RequestLoginEmail):
 try:
    email = request.email
    password = request.password
    check_email_fc = sf.check_email_empty_invalid(email)
    if check_email_fc is not True:
        return check_email_fc
    if password is None:
        return res.ReponseError(
            status=400,
            data=res.Message(message="Password is empty")
        )
    user_check = get_user1(email)
    if user_check is None:
        return res.ReponseError(
            status=404,
            data=res.Message(message="Email not exist")
        )
    user = sign_in_with_email_and_password(email, password)

    if user:
        check = signJWT(user)
        if check is False:
            return res.ReponseError(
                status=500,
                data=res.Message(message="Invalid authorization code.")
            )
        else:
            access_token = check["access_token"]
            refresh_token = check["refresh_token"]
            expires_in = check["expires_in"]
            session_id = check["session_id"]
            return res.ResponseLoginEmail(
                status=200,
                data=res.DataLogin(access_token=access_token, refresh_token=refresh_token, expires_in=expires_in,
                                         session_id=session_id)
            )
    else:
        return res.ReponseError(
            status=400,
            data=res.Message(message="Passwords do not match")
        )
 except:
    return res.ReponseError(
        status=500,
        data=res.Message(message="Server Error")
    )

def verify_token_google(token):
    from google.oauth2 import id_token
    from google.auth.transport import requests
    try:
        CLIENT_ID = CLIENT_ID_GOOGLE
        id_info = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
        check = id_info['email_verified']
        if check is True:
            return True
    except ValueError as e:
        return False

async def login_google(request: req.RequestLoginGoogle):
  try:
    email = request.email
    token_google = request.token_google
    check_google = verify_token_google(token_google)
    if check_google is False:
        return res.ReponseError(
            status=400,
            data =res.Message(message="Login google failed")
        )
    check_email_fc = sf.check_email_empty_invalid(email)
    if check_email_fc is not True:
        return check_email_fc
    user = get_user1(email)
    if user:
     check = signJWT(email)
     if check == False:
         return res.ReponseError(
            status=500,
            data =res.Message(message="Invalid authorization code.")
        )
     else:
         access_token = check["access_token"]
         refresh_token = check["refresh_token"]
         expires_in = check["expires_in"]
         session_id = check["session_id"]
         return res.ResponseLoginGoogle(
           status= 200,
           data = res.DataLogin(access_token=access_token,refresh_token=refresh_token,expires_in=expires_in,session_id=session_id)
    )
    else:
          return res.ReponseError(
            status= 404,
            data = res.Message(message="Email not exist")
        )
  except:
      return res.ReponseError(
            status=500,
            data=res.Message(message="Server Error")
        )

async def sign_up(request: req.RequestRegister):
 try:
    email = request.email
    password = request.password
    confirm_password = request.confirm_password
    username = request.username
    check_email_fc = sf.check_email_empty_invalid(email)
    if check_email_fc is not True:
        return check_email_fc
    if password is None or password == "":
        return res.ReponseError(
            status=400,
            data =res.Message(message="password is empty")
        )
    if confirm_password is None or confirm_password == "":
        return res.ReponseError(
            status=400,
            data =res.Message(message="confirm password is empty")
        )
    if confirm_password != password:
        return res.ReponseError(status=400,
                                      data =res.Message(message="password and confirm_password do not match"))
    user_signup = get_user1(email)
    if user_signup is not None:
        return res.ReponseError(
            status=400,
            data =res.Message(message="Email exist")
        )

    user_info, display_name = sign_up_with_email_and_password(email, password, username)
    if user_info:
       return res.ResponseSignUp(
            status=200,
            data =res.DataSignUp(email=user_info)
        )
    else:
        return res.ReponseError(
            status=500,
            data =res.Message(message="Internal Server Error")
        )
 except:
     return res.ReponseError(
            status=500,
            data=res.Message(message="Server Error")
        )

import pytz, datetime
import auth.authentication as auth123
from response import ResponseDefault as res1
def refresh_token(request: req.RequestRefreshTokenLogin):
     try:
         token = request.refresh_token
         if token is None:
             return res.ReponseError(
                 status=400,
                 data=res.Message(message="token is empty")
             )
         user_token = UserRepository.getUserIdByRefreshToken(token)
         if user_token is None:
             return res.ReponseError(
                 status=404,
                 data=res_login.Message(message="Not found refresh token")
             )
         email = UserRepository.getEmailUserById(user_token)
         if email:
             rf_token = token
         result = auth123.get_refresh_token(token, email)
         token_new = result["access_token"]
         rf_token_new = result["refresh_token"]
         seconds1 = result["expires_in"]
         session_id = result["session_id"]
         vn_timezone = pytz.timezone('Asia/Ho_Chi_Minh')
         current_time = datetime.datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(vn_timezone) + timedelta(
             seconds=seconds1)
         formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S ')
         if rf_token == rf_token_new:
             UserRepository.updateAccessToken(user_token, token_new, formatted_time)
         else:
             UserRepository.UpdateAccessTokenRefreshTokenById(user_token, token_new, rf_token_new, formatted_time)
         user = token_new
         if user == False:
             return res.ReponseError(
                 status=400,
                 data=res.Message(message="Refresh token error")
             )
         return res.ResponseRefreshTokenLogin(
             status=200,
             data=res.DataRefreshToken(token_new=user, session_id=session_id)
         )
     except:
         return res.ReponseError(
             status=500,
             data=res.Message(message="Server Error")
         )
def check_token_is_valid(token):
   try:
    check = UserRepository.getEmailUserByAccessToken(token)
    if check is None:
        return False
    return True
   except:
       return res.ReponseError(
           status=500,
           data=res.Message(message="Server Error")
       )