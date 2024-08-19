from datetime import timedelta,datetime
from request import RequestOTP as req
from response import ResponseOTP as res
import re
from firebase_admin import auth, exceptions
from repository import OTPRepository
from datetime import datetime, timedelta
import datetime, string,random
from function import  support_function as sf
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
    
def generate_otp(length=6):
    characters = string.ascii_uppercase + string.digits
    otp = ''.join(random.choice(characters) for _ in range(length))
    return otp

async def createOTP(request: req.RequestCreateOTP):
  try:
    email = request.email
    otp = generate_otp()
    check_email_fc = sf.check_email_empty_invalid(email)
    if check_email_fc is not True:
        return check_email_fc
    OTPRepository.addOTP(email,otp)
    return res.ResponseCreateOTP(
            status=200,
            data = res.CheckModel(check=True),
            otp = otp
        )
  except:
      return res.ReponseError(
            status=500,
            data=res.Message(message="Server Error")
        )

async def verifyOTP(request: req.RequestVerifyOTP):
 try:
    email = request.email
    otp = request.otp
    check_email_fc = sf.check_email_empty_invalid(email)
    if check_email_fc is not True:
        return check_email_fc
    if otp is None:
        return res.ReponseError(
            status=400,
            data=res.Message(message="otp is empty")
        ) 
    user_otp = OTPRepository.getOtpByEmail(email)
    if user_otp:
        otp_db = user_otp.otp
        otp_created_at = user_otp.created_at
        if otp == otp_db:
            current_time = datetime.datetime.now()
            otp_expiry_time = otp_created_at + timedelta(minutes=15)
            if current_time <= otp_expiry_time:
                OTPRepository.deleteOTP(email, otp)
                return res.ResponseVerifyOTPSignUp(
                    status=200,
                    data=res.Message(message="OTP is valid")
                )
            else:
                return res.ReponseError(
                    status=400,
                    data=res.Message(message="OTP has expired")
                )
        else:
            return res.ReponseError(
                status=400,
                data=res.Message(message="Invalid OTP")
            )
    else:
        return res.ReponseError(
            status=404,
            data=res.Message(message="No OTP found for this email")
        )
 except:
     return res.ReponseError(
            status=500,
            data=res.Message(message="Server Error")
        )

async def createOTPReset(email):
 try:
    otp = generate_otp()
    check_email_fc = sf.check_email_empty_invalid(email)
    if check_email_fc is not True:
        return check_email_fc
    OTPRepository.addOTP(email,otp)
    return res.ResponseCreateOTP(
            status=200,
            data = res.CheckModel(check=True),
            otp = otp
        )
 except:
     return res.ReponseError(
            status=500,
            data=res.Message(message="Server Error")
        )

async def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for i in range(length))
    return password

async def verifyOTPReset(request: req.RequestVerifyOTP):
 try:
    email = request.email
    otp = request.otp
    check_email_fc = sf.check_email_empty_invalid(email)
    if check_email_fc is not True:
        return check_email_fc
    if otp is None:
        return res.ReponseError(
            status=400,
            data=res.Message(message="OTP is empty")
        ) 
    user_otp = OTPRepository.getOtpByEmail(email)
    if user_otp:
        otp_db = user_otp.otp
        otp_created_at = user_otp.created_at
        if otp == otp_db:
            current_time = datetime.datetime.now()  # Lấy thời gian hiện tại với múi giờ hệ thống (múi giờ +7)
            otp_expiry_time = otp_created_at + timedelta(minutes=15)
            new_password = generate_random_password()
            if current_time <= otp_expiry_time:
                OTPRepository.deleteOTP(email, otp)
                user_email = auth.get_user_by_email(email)
                auth.update_user(
                    user_email.uid,
                    password=new_password)
                return res.ResponseVerifyOTP(
                    status=200,
                    data=res.Message(message="New Password send to Email"),
                    newpassword=new_password
                )
            else:
                return res.ReponseError(
                    status=400,
                    data=res.Message(message="OTP has expired")
                )
        else:
            return res.ReponseError(
                status=400,
                data=res.Message(message="Invalid OTP")
            )
    else:
        return res.ReponseError(
            status=404,
            data=res.Message(message="No OTP found for this email")
        )
 except:
     return res.ReponseError(
            status=500,
            data=res.Message(message="Server Error")
        )