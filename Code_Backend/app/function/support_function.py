from pydantic.error_wrappers import ErrorWrapper
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from service import MySQLService,UserService,ChatService
from request import RequestMySQL,RequestUser,RequestDefault
from auth.authentication import decodeJWT
from repository import UserRepository
from auth import authentication
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, Form, File, UploadFile
from typing import List
from service import FileService,DefaultService,UserService
from request import RequestFile,RequestChat,RequestDefault
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic.error_wrappers import ErrorWrapper
import json
from function import support_function
from repository import UserRepository
from response import ResponseDefault as res
import re

def is_positive_integer(value):
    if isinstance(value, int) and value > 0:
        return True
    else:
        return False

def check_value_user_id_controller(user_id: str):
    if user_id is None or user_id.strip() == "":
        return res.ReponseError(status=400,
                                data=res.Message(message="user_id field is required."))
    user_id = user_id.strip("'").strip('"')
    try:
        user_id_int = int(user_id)
    except ValueError:
        return res.ReponseError(status=400,
                                data=res.Message(message="user_id must be an integer"))

    if not support_function.is_positive_integer(user_id_int):
        return res.ReponseError(status=400,
                                data=res.Message(message="user_id must be greater than 0"))
    return True

def check_value_user_id(user_id: str, current_user_email: str):
    if user_id is None or user_id.strip() == "":
        return res.ReponseError(status=400,
                                data=res.Message(message="user_id field is required."))
    user_id = user_id.strip("'").strip('"')
    try:
        user_id_int = int(user_id)
    except ValueError:
        return res.ReponseError(status=400,
                                data=res.Message(message="user_id must be an integer"))

    if not support_function.is_positive_integer(user_id_int):
        return res.ReponseError(status=400,
                                data=res.Message(message="user_id must be greater than 0"))
    email = UserRepository.getEmailUserByIdFix(user_id)
    if email is None:
        return res.ReponseError(status=404,
                                data=res.Message(message="user_id not exist"))
    email = email[0]
    if email != current_user_email:
        raise HTTPException(status_code=403, detail="Sorry, you can't perform actions with this user id.")
    return True

def check_value_email_controller(email: str):
    if email is None or email.strip() == "":
        return res.ReponseError(status = 400,
                                data = res.Message(message="Email is required."))
    try:
        int(email)
        return res.ReponseError(status=400,
                                data=res.Message(message="Email must be a string, not a number."))
    except ValueError:
        pass
    return True

def check_value_otp(otp: str):
    if otp is None:
        return res.ReponseError(status=400,
                                data=res.Message(message="OTP is required"))
    if otp.isdigit():
        return res.ReponseError(status=400,
                                data=res.Message(message="OTP must be a string, not a number."))
    if len(otp) != 6:
        return res.ReponseError(status=400,
                                data=res.Message(message="OTP max length is 6"))
    return True

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
def check_email(email):
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False
def check_email_service(user_id: str):
    email1 = UserRepository.getEmailUserByIdFix(user_id)
    if email1 is None:
        return res.ReponseError(
            status=404,
            data=res.Message(message="Id not exist")
        )
    email = email1[0]
    if email is None:
        return res.ReponseError(
            status=400,
            data=res.Message(message="Email is empty")
        )
    if check_email(email) == False:
        return res.ReponseError(
            status=400,
            data=res.Message(message="Email invalid")
        )
    return email

def check_email_empty_invalid(email: str):
    if email is None or email == "":
        return res.ReponseError(
            status=400,
            data=res.Message(message="Email is empty")
        )
    if check_email(email) == False:
        return res.ReponseError(
            status=400,
            data =res.Message(message="Email invalid")
        )
    return True