import time
from typing import Dict
import jwt
import secrets
import logging
from fastapi import Depends, HTTPException
import base64
from datetime import datetime, timedelta
from repository import UserRepository, UserLoginRepository
import string, random

def check_token_is_valid(token):
    check = UserRepository.getEmailUserByAccessToken(token)
    if check is None:
        return False
    return True

def unique_string(byte: int = 8) -> str:
    return secrets.token_urlsafe(byte)
JWT_SECRET = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
JWT_ALGORITHM = "HS512"
SECRET_KEY= "8deadce9449770680910741063cd0a3fe0acb62a8978661f421bbcbb66dc41f1"

def token_response(token: str):
    return {
        "access_token": token
    }
def str_encode(string: str) -> str:
    return base64.b85encode(string.encode('ascii')).decode('ascii')

def get_token_payload(token: str, secret: str, algo: str):
    try:
        payload = jwt.decode(token, secret, algorithms=algo)
    except Exception as jwt_exec:
        logging.debug(f"JWT Error: {str(jwt_exec)}")
        payload = None
    return payload

from datetime import datetime
def generate_token(payload: dict, secret: str, algo: str, expiry: timedelta):
    expire = datetime.now() + expiry
    payload.update({"exp": expire})
    return jwt.encode(payload, secret, algorithm=algo)

def str_decode(string: str) -> str:
    return base64.b85decode(string.encode('ascii')).decode('ascii')

def generate_random_string(length=12):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for i in range(length))
    return random_string

import pytz
from datetime import datetime
def signJWT(user_email: str) -> Dict[str, str]:
    rt_expires = timedelta(days=3)
    refresh_key = unique_string(100)
    access_key = unique_string(50)
    at_expires = timedelta(minutes=180)
    at_payload = {
        "sub": str_encode(str(user_email)),
        'a': access_key,
    }
    access_token = generate_token(at_payload, JWT_SECRET, JWT_ALGORITHM, at_expires)
    rt_payload = {"sub": str_encode(str(user_email)), "t": refresh_key, 'a': access_key}
    refresh_token = generate_token(rt_payload, SECRET_KEY,JWT_ALGORITHM, rt_expires)
    expires_in = at_expires.seconds
    vn_timezone = pytz.timezone('Asia/Ho_Chi_Minh')
    current_time = datetime.now().replace(tzinfo=pytz.utc).astimezone(vn_timezone) + timedelta(seconds=expires_in)
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S ')
    existing_user = UserRepository.getUserByEmail(user_email)
    if existing_user is None:
        UserRepository.addUser(user_email, access_token, refresh_token, formatted_time)
    else:
        UserRepository.updateUserLogin(user_email, access_token, refresh_token, formatted_time)
    user_record = UserRepository.getUserByEmail(user_email)
    session_id = ""
    if user_record:
        session_id = generate_random_string()
        existing_userlogin = UserLoginRepository.getUserLogin(user_email)
        if existing_userlogin is None:
            UserLoginRepository.addUserLogin(user_email,session_id=session_id)
        else:
            UserLoginRepository.updateUserLogin(user_email, session_id)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": at_expires.seconds,
        "session_id": session_id
     }

def returnAccessToken(user_email: str, refresh_token: str) -> Dict[str, str]:
    access_key = unique_string(50)
    at_expires = timedelta(minutes=180)
    at_payload = {
        "sub": str_encode(str(user_email)),
        'a': access_key,
    }
    access_token = generate_token(at_payload, JWT_SECRET, JWT_ALGORITHM, at_expires)
    user_record = UserRepository.getUserByEmail(user_email)
    session_id = ""
    if user_record:
        email1 = user_record.email
    if email1:
        session_id = generate_random_string()
        existing_userlogin = UserLoginRepository.getUserLogin(user_email)
        if existing_userlogin is None:
            UserLoginRepository.addUserLogin(user_email,session_id=session_id)
        else:
            UserLoginRepository.updateUserLogin(user_email,session_id)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": at_expires.seconds,
        "session_id": session_id
    }

def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except:
        return {}
    
def get_refresh_token(refresh_token, email):
    token_payload = get_token_payload(refresh_token, SECRET_KEY, JWT_ALGORITHM)
    if not token_payload:
        raise HTTPException(status_code=403, detail="Invalid Request.")
    exp = token_payload.get('exp')
    if exp >= time.time() and token_payload:
       return returnAccessToken(email,refresh_token)
    elif not token_payload:
       return signJWT(email)