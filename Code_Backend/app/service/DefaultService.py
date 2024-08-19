from typing import Union
from datetime import timedelta
from request import RequestDefault as req
from response import ResponseDefault as res
from response import ResponseUser as res_login
from firebase_admin import credentials, auth, exceptions
import firebase_admin
import base64
import auth.authentication as auth123
import re
from repository import UserRepository, UserInfoRepository
from pathlib import Path
import cloudinary
import cloudinary.uploader
from fastapi import FastAPI, File, UploadFile
from function import support_function as sf
from dotenv import load_dotenv
from service import AuthService as authservice
import os
load_dotenv()
CLOUDINARY_CLOUD_NAME=os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY=os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET=os.getenv("CLOUDINARY_API_SECRET")

cloudinary.config(
     cloud_name=CLOUDINARY_CLOUD_NAME,
     api_key=CLOUDINARY_API_KEY,
     api_secret=CLOUDINARY_API_SECRET
)
import os

try:
 if not firebase_admin._apps:
    cred = credentials.Certificate("../certificate/firebase_certificate.json")
    fred = firebase_admin.initialize_app(cred)
except:
   try:
    if not firebase_admin._apps:
     cred = credentials.Certificate("firebase_certificate.json")
     fred = firebase_admin.initialize_app(cred)
   except:
    if not firebase_admin._apps:
     json_path = Path(__file__).resolve().parent / 'app' / 'firebase_certificate.json'
     cred = credentials.Certificate(str(json_path))
     fred = firebase_admin.initialize_app(cred)

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

def check_email(email):
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

def get_user(email):
    try:
        user = auth.get_user_by_email(email)
        return user
    except exceptions.FirebaseError as e:
        return None
        
def create_user(email):
    user = auth.create_user(email=email)
    return user

def get_user1(email):
    try:
        user = auth.get_user_by_email(email)
        return user
    except exceptions.FirebaseError as e:
        return None

async def create_firebase_user(request: req.RequestCreateFireBaseUserGoogle):
    try:
     email = request.email
     token_google = request.token_google
     check_email_fc = sf.check_email_empty_invalid(email)
     if check_email_fc is not True:
        return check_email_fc
     user = get_user(email)
     if token_google is None or token_google == "":
         return res.ReponseError(
             status=400,
             data=res.Message(message="token google not empty")
         )
     check_google = authservice.verify_token_google(token_google)
     if check_google == False:
         return res.ReponseError(
             status=400,
             data=res.Message(message="Create user failed")
         )
     if user: 
        email1 = user.email
        display_name = user.display_name
        uid = user.uid
        photo_url = user.photo_url
        return res.ResponseCreateFireBaseUser(
           status=200,
           data = res.DataCreateFireBaseUser(localId=uid,
                                             email=email1,
                                             displayName=display_name,
                                             photoUrl=photo_url)
    )
     else:
        return res.ReponseError(
            status=500,
            data =res.Message(message="Error")
        ) 
    except:
        return res.ReponseError(
            status=500,
            data =res.Message(message="Server Error")
        )

async def info_user(request: req.RequestInfoUser):
    try:
        user_id = request.user_id
        email = sf.check_email_service(user_id)
        if isinstance(email, res.ReponseError):
            return email
        user = get_user(email)
        if user is None:
            return res.ReponseError(
                status=404,
                data=res.Message(message="User not found")
            )
        uid = user.uid if user.uid else ""
        email = user.email if user.email else ""
        display_name = user.display_name if user.display_name else "N/A"
        photo_url = user.photo_url if user.photo_url else "N/A"
        return res.ResponseInfoUser(
            status=200,
            data=res.DataInfoUser(
                uid=uid,
                email=email,
                display_name=display_name,
                photo_url=photo_url
            )
        )
    except Exception as e:
        return res.ReponseError(
            status=500,
            data=res.Message(message="Server Error: " + str(e))
        )

def check_email_token(token):
  try:
    decoded_token = auth123.decodeJWT(token)
    sub_value = decoded_token.get("sub")
    name_user = base64.b85decode(sub_value.encode('ascii')).decode('ascii')
    return name_user
  except:
    return False

async def is_me(request: req.RequestIsMe):
 try:
   token = request.token
   if token is None or token == "":
          return res.ReponseError(
            status=400,
            data =res.Message(message="token is empty")
        )
   test = check_email_token(token)
   if test is not False:
      user_id = UserRepository.getUserByEmail(test).id
      return res.ResponseIsMe(
           status=200,
           data = res.DataIsMe(user_id = user_id))
 except:
    return res.ReponseError(
            status=500,
            data=res.Message(message="Server Error")
        )

ALLOWED_EXTENSIONS = {'png', 'jpg','jpeg'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

async def upload_image_service(request: req.RequestUpLoadImage):
  try:
        user_id = request.user_id
        file = request.files
        email = sf.check_email_service(user_id)
        if isinstance(email, res.ReponseError):
            return email
        if not allowed_file(file.filename):
            return res.ReponseError(
                status=415,
                data=res.Message(message=f"File type not allow")
            )
        temp_file_path = f"temp_image_{email}.png"
        contents = file.file.read()
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(contents)
        upload_result = cloudinary.uploader.upload(temp_file_path, public_id=email)
        os.remove(temp_file_path)
        return res.ResponseUploadImage(
          status=200,
          data=res.DataUploadImage(url=upload_result["secure_url"])
    )
  except:
      return res.ReponseError(
          status=500,
          data=res.Message(message="Server Error")
      )