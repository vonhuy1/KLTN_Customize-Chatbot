from fastapi import APIRouter
from function import support_function
from request import RequestOTP
from service import OTPService
from fastapi import HTTPException
from pydantic.error_wrappers import ErrorWrapper
from pydantic import BaseModel
from response import ResponseOTP as res
router = APIRouter()

@router.post('/create_otp', tags=["OTP"])
async def create_otp(request:  RequestOTP.RequestCreateOTP):
    email = request.email
    check = support_function.check_value_email_controller(email)
    if check is not True:
        return check
    return await OTPService.createOTP(request)

@router.post('/verify_otp', tags=["OTP"])
async def verify_otp(request:  RequestOTP.RequestVerifyOTP):
    check = support_function.check_value_email_controller(request.email)
    if check is not True:
        return check
    check_otp = support_function.check_value_otp(request.otp)
    if check_otp is not True:
        return check_otp
    return await OTPService.verifyOTP(request)

@router.post('/verify_otp_reset_password', tags=["OTP"])
async def verify_otp_reset(request: RequestOTP.RequestVerifyOTP):
    check = support_function.check_value_email_controller(request.email)
    if check is not True:
        return check
    check_otp = support_function.check_value_otp(request.otp)
    if check_otp is not True:
        return check_otp
    return await OTPService.verifyOTPReset(request)