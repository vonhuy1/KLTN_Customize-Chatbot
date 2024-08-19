import os
import sys
from unittest.mock import patch, MagicMock

from fastapi.testclient import TestClient

app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, app_path)
from controller import OTPController
client = TestClient(OTPController.router)

@patch('service.OTPService.check_email')
@patch('service.OTPService.get_user1')
@patch('repository.OTPRepository.addOTP')
@patch('service.OTPService.generate_otp')
@patch('service.OTPService.sf')
def test_createOTPReset_success(mock_support_function, mock_generate_otp,mock_addOTP, mock_get_user1, mock_check_email):
        mock_get_user1.return_value = MagicMock()
        email = "user@example.com"
        mock_support_function.check_email_empty_invalid.return_value = True
        mock_generate_otp.return_value = "123456"
        response = client.post("/create_otp", json={"email": email})
        assert response.json()['status'] == 200
        assert response.json()['data']['check'] == True
        assert response.json()['otp'] == "123456"


def test_createOTPReset_email_empty():
        email = ""
        response = client.post("/create_otp", json={"email": email})
        assert response.json()['status'] == 400
        assert response.json()['data']['message'] == "Email is required."


def test_createOTPReset_email_invalid():
        email = "201333"
        response =client.post("/create_otp", json={"email": email})
        assert response.json()['status'] == 400
        assert response.json()['data']['message'] == "Email must be a string, not a number."

@patch('service.OTPService.generate_otp')
@patch('service.OTPService.check_email')
@patch('repository.OTPRepository.addOTP')
@patch('service.OTPService.sf')
def test_createOTP_success(mock_support_function,mock_addOTP, mock_check_email, mock_generate_otp):
        mock_generate_otp.return_value = "123AB6"
        email = "20133118@gmail.com"
        otp = "123AB6"
        mock_support_function.check_email_empty_invalid.return_value = True
        mock_addOTP(email,otp)
        response =client.post("/create_otp", json={"email": email})
        assert response.json()['status'] == 200
        assert response.json()['data']['check'] == True
        assert response.json()['otp'] == "123AB6"

def test_createOTP_failed_empty_email():
        email = ""
        response =client.post("/create_otp", json={"email": email})
        assert response.json()['status'] == 400
        assert response.json()['data']['message'] == "Email is required."


def test_createOTP_failed_empty_invalid():
        email = "20133"
        response =client.post("/create_otp", json={"email": email})
        assert response.json()['status'] == 400
        assert response.json()['data']['message'] == "Email must be a string, not a number."
from datetime import datetime,timedelta
@patch('service.OTPService.sf.check_email_empty_invalid', return_value=True)
@patch('repository.OTPRepository.getOtpByEmail')
@patch('repository.OTPRepository.deleteOTP')
def test_verifyOTP_success(mock_deleteOTP, mock_getOtpByEmail, mock_check_email):
        current_time = datetime.now()
        mock_getOtpByEmail.return_value = MagicMock(otp="abcdef", created_at=current_time - timedelta(minutes=5))
        email = "user@example.com"
        otp = "abcdef"
        response = client.post("/verify_otp", json={"email": email,"otp": otp})
        mock_deleteOTP(email,otp)
        assert response.json()['status'] == 200
        assert response.json()['data']['message'] == "OTP is valid"

@patch('service.OTPService.sf.check_email_empty_invalid', return_value=True)
@patch('repository.OTPRepository.getOtpByEmail')
def test_verifyOTP_failed_invalid_otp(mock_getOtpByEmail, mock_check_email):
        current_time = datetime.now()
        mock_getOtpByEmail.return_value = MagicMock(otp="654321", created_at=current_time - timedelta(minutes=5))
        email = "user@example.com"
        otp = "123456"
        response =client.post("/verify_otp", json={"email": email,"otp": otp})
        assert response.json()['status'] == 400
        assert response.json()['data']['message'] == "OTP must be a string, not a number."

def test_verifyOTP_failed_invalid_email():
        email = "invalidemail"
        otp = "123456"
        response =client.post("/verify_otp", json={"email": email,"otp": otp})
        assert response.json()['status'] == 400
        assert response.json()['data']['message'] == "OTP must be a string, not a number."

def test_verifyOTP_failed_empty_email():
        email = None
        otp = "123456"
        response =client.post("/verify_otp", json={"email": email,"otp": otp})
        assert response.json()['status'] == 400
        assert response.json()['data']['message'] == "Email is required."


def test_verifyOTP_failed_empty_otp():
        email = "user@example.com"
        otp = None
        response = client.post("/verify_otp", json={"email": email,"otp": otp})
        assert response.json()['status'] == 400
        assert response.json()['data']['message'] == "OTP is required"

@patch('service.OTPService.sf.check_email_empty_invalid', return_value=True)
@patch('repository.OTPRepository.getOtpByEmail')
def test_verifyOTP_failed_no_otp_found(mock_getOtpByEmail, mock_check_email):
        mock_getOtpByEmail.return_value = None
        email = "user@example.com"
        otp = "1234ab"
        response =client.post("/verify_otp", json={"email": email,"otp": otp})
        assert response.json()['status'] == 404
        assert response.json()['data']['message'] == "No OTP found for this email"

@patch('service.OTPService.sf.check_email_empty_invalid', return_value=True)
@patch('repository.OTPRepository.getOtpByEmail')
def test_verifyOTP_has_expired( mock_getOtpByEmail, mock_check_email):
        current_time = datetime.now()
        mock_getOtpByEmail.return_value = MagicMock(otp="1234ab", created_at=current_time - timedelta(minutes=100))
        email = "user@example.com"
        otp = "1234ab"
        response =client.post("/verify_otp", json={"email": email,"otp": otp})
        assert response.json()['status'] == 400
        assert response.json()['data']['message'] == "OTP has expired"

@patch('service.OTPService.sf.check_email_empty_invalid', return_value=True)
@patch('repository.OTPRepository.getOtpByEmail')
@patch('repository.OTPRepository.deleteOTP')
@patch('service.OTPService.auth.get_user_by_email')
@patch('service.OTPService.auth')
@patch('service.OTPService.generate_random_password')
def test_verifyOTPReset1_success( mock_generate_password,mock_update_user, mock_get_user_by_email, mock_deleteOTP, mock_getOtpByEmail, mock_check_email):
        current_time = datetime.now()
        mock_getOtpByEmail.return_value = MagicMock(otp="abcd12", created_at=current_time - timedelta(minutes=5))
        mock_get_user_by_email.return_value = MagicMock(uid="12345")
        email = "user@example.com"
        otp = "abcd12"
        mock_generate_password.return_value = "ABC123"
        mock_update_user.update_user(uid="12345",)
        mock_deleteOTP("user@example.com", "abcd12")
        response = client.post("/verify_otp_reset_password", json={"email": email,"otp": otp})
        assert response.json()['status'] == 200
        assert response.json()['data']['message'] == "New Password send to Email"
        assert response.json()['newpassword'] == "ABC123"

@patch('service.OTPService.sf.check_email_empty_invalid', return_value=True)
@patch('repository.OTPRepository.getOtpByEmail')
def test_verifyOTPReset_failed_invalid_otp(mock_getOtpByEmail, mock_check_email):
        current_time = datetime.now()
        mock_getOtpByEmail.return_value = MagicMock(otp="654321", created_at=current_time - timedelta(minutes=5))
        email = "user@example.com"
        otp = "abcd12"
        response =client.post("/verify_otp_reset_password", json={"email": email,"otp": otp})
        assert response.json()['status'] == 400
        assert response.json()['data']['message'] == "Invalid OTP"

@patch('service.OTPService.sf.check_email_empty_invalid', return_value=True)
@patch('repository.OTPRepository.getOtpByEmail')
def test_verifyOTPReset_failed_no_otp_found(mock_getOtpByEmail, mock_check_email):
        mock_getOtpByEmail.return_value = None
        email = "user@example.com"
        otp = "abcd12"
        response = client.post("/verify_otp_reset_password", json={"email": email,"otp": otp})
        assert response.json()['status'] == 404
        assert response.json()['data']['message'] == "No OTP found for this email"

@patch('service.OTPService.sf.check_email_empty_invalid', return_value=True)
@patch('repository.OTPRepository.getOtpByEmail')
def test_verifyOTPReset_has_expired(mock_getOtpByEmail, mock_check_email):
        current_time = datetime.now()
        mock_getOtpByEmail.return_value = MagicMock(otp="1234ab", created_at=current_time - timedelta(minutes=100))
        email = "vonhuy@gmail.com"
        otp = "1234ab"
        response = client.post("/verify_otp_reset_password", json={"email": email,"otp": otp})
        assert response.json()['status'] == 400
        assert response.json()['data']['message'] == "OTP has expired"

def test_verifyOTPReset_failed_invalid_email():
        email = "invalidemail"
        otp = "abcd12"
        response =client.post("/verify_otp_reset_password", json={"email": email,"otp": otp})
        assert response.json()['status'] == 400
        assert response.json()['data']['message'] == "Email invalid"


def test_verifyOTPReset_failed_empty_email():
        email = None
        otp = "123456"
        response =client.post("/verify_otp_reset_password", json={"email": email,"otp": otp})
        assert response.json()['status'] == 400
        assert response.json()['data']['message'] == "Email is required."


def test_verifyOTPReset_failed_empty_otp():
        email = "user@example.com"
        otp = None
        response = client.post("/verify_otp_reset_password", json={"email": email,"otp": otp})
        assert response.json()['status'] == 400
        assert response.json()['data']['message'] == "OTP is required"


def test_createOTP_email_required():
        email = None
        response = client.post("/create_otp", json={"email": email})
        assert response.json()['status'] == 400
        assert response.json()['data']['message'] == "Email is required."

def test_createOTP_email_must_be_string():
        email = "20133"
        response = client.post("/create_otp", json={"email": email})
        assert response.json()['status'] == 400
        assert response.json()['data']['message'] == "Email must be a string, not a number."

def test_verifyOTP_email_is_required():
        email = None
        otp ="123abc"
        response = client.post("/verify_otp", json={"email": email,"otp": otp})
        assert response.json()['status'] == 400
        assert response.json()['data']['message'] == "Email is required."

def test_verifyOTP_otp_is_required():
        email = "test@gmail.com"
        otp = None
        response = client.post("/verify_otp", json={"email": email,"otp": otp})
        assert response.json()['status'] == 400
        assert response.json()['data']['message'] == "OTP is required"

def test_verifyOTP_otp_email_must_be_string():
        email = "20133"
        otp = "123abc"
        response = client.post("/verify_otp", json={"email": email,"otp": otp})
        assert response.json()['status'] == 400
        assert response.json()['data']['message'] == "Email must be a string, not a number."

def test_verifyOTP_otp_must_be_string():
        email = "20133@gmail.com"
        otp = "123456"
        response = client.post("/verify_otp", json={"email": email,"otp": otp})
        assert response.json()['status'] == 400
        assert response.json()['data']['message'] == "OTP must be a string, not a number."

def test_verifyOTP_otp_max_length():
        email = "20133@gmail.com"
        otp = "abcdef1"
        response = client.post("/verify_otp", json={"email": email,"otp": otp})
        assert response.json()['status'] == 400
        assert response.json()['data']['message'] == "OTP max length is 6"

def test_verifyOTPReset_email_is_required():
        email = None
        otp ="123abc"
        response = client.post("/verify_otp_reset_password", json={"email": email,"otp": otp})
        assert response.json()['status'] == 400
        assert response.json()['data']['message'] == "Email is required."

def test_verifyOTPReset_otp_is_required():
        email = "test@gmail.com"
        otp = None
        response = client.post("/verify_otp_reset_password", json={"email": email,"otp": otp})
        assert response.json()['status'] == 400
        assert response.json()['data']['message'] == "OTP is required"

def test_verifyOTPReset_otp_email_must_be_string():
        email = "20133"
        otp = "123abc"
        response = client.post("/verify_otp_reset_password", json={"email": email,"otp": otp})
        assert response.json()['status'] == 400
        assert response.json()['data']['message'] == "Email must be a string, not a number."

def test_verifyOTPReset_otp_must_be_string():
        email = "20133@gmail.com"
        otp = "123456"
        response = client.post("/verify_otp_reset_password", json={"email": email,"otp": otp})
        assert response.json()['status'] == 400
        assert response.json()['data']['message'] == "OTP must be a string, not a number."

def test_verifyOTPReset_otp_max_length():
        email = "20133@gmail.com"
        otp = "abcdef1"
        response = client.post("/verify_otp_reset_password", json={"email": email,"otp": otp})
        assert response.json()['status'] == 400
        assert response.json()['data']['message'] == "OTP max length is 6"