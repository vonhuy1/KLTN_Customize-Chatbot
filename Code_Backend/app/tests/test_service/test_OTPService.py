import unittest
import sys
import os
app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, app_path)
from request import RequestOTP as req
from response import ResponseOTP as res
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from service.OTPService import createOTP, verifyOTP, createOTPReset, verifyOTPReset

class TestCreateOTPReset(unittest.TestCase):
    @patch('service.OTPService.check_email')
    @patch('service.OTPService.get_user1')
    @patch('service.OTPService.OTPRepository.addOTP')
    @patch('service.OTPService.generate_otp')
    @patch('service.OTPService.sf')
    def test_createOTPReset_success(self,mock_support_function, mock_generate_otp, mock_addOTP, mock_get_user1, mock_check_email):
        mock_get_user1.return_value = MagicMock()
        email = "user@example.com"
        mock_support_function.check_email_empty_invalid.return_value = True
        mock_generate_otp.return_value = "123456"
        response = createOTPReset(email)
        self.assertEqual(response.status, 200)
        self.assertEqual(response.data.check, True)
        self.assertEqual(response.otp, "123456")

    @patch('service.OTPService.check_email')
    @patch('service.OTPService.get_user1')
    @patch('service.OTPService.OTPRepository.addOTP')
    @patch('service.OTPService.sf')
    def test_createOTPReset_email_empty(self,mock_support_function, mock_addOTP, mock_get_user1, mock_check_email):
        email = None
        mock_support_function.check_email_empty_invalid.return_value = res.ReponseError(status=400, data=res.Message(
            message="Email is empty"))
        response = createOTPReset(email)
        self.assertIsInstance(response, res.ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data, res.Message(message='Email is empty'))

    @patch('service.OTPService.check_email')
    @patch('service.OTPService.sf')
    def test_createOTPReset_email_invalid(self,mock_support_function, mock_check_email):
        email = "201333"
        mock_support_function.check_email_empty_invalid.return_value = res.ReponseError(status=400, data=res.Message(
            message="Email invalid"))
        response = createOTPReset(email)
        self.assertIsInstance(response, res.ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data, res.Message(message='Email invalid'))

class TestCreateOTPFunctions(unittest.TestCase):
    @patch('service.OTPService.generate_otp')
    @patch('service.OTPService.check_email')
    @patch('service.OTPService.OTPRepository')
    @patch('service.OTPService.sf')
    def test_createOTP_success(self,mock_support_function, mock_addOTP, mock_check_email, mock_generate_otp):
        mock_generate_otp.return_value = "123AB6"
        email = "20133118@gmail.com"
        otp = "123AB6"
        mock_support_function.check_email_empty_invalid.return_value = True
        mock_addOTP.addOTP(email, otp)
        request = req.RequestCreateOTP(email=email)
        response = createOTP(request)
        self.assertIsInstance(response, res.ResponseCreateOTP)
        self.assertEqual(response.status, 200)
        self.assertTrue(response.data.check)
        self.assertEqual(response.otp, "123AB6")

    @patch('service.OTPService.check_email')
    @patch('service.OTPService.sf')
    def test_createOTP_failed_empty_email(self,mock_support_function, mock_check_email):
        email = None
        mock_support_function.check_email_empty_invalid.return_value = res.ReponseError(status=400, data=res.Message(
            message="Email is empty"))
        request = req.RequestCreateOTP(email=email)
        response = createOTP(request)
        self.assertIsInstance(response, res.ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message, "Email is empty")
        
    @patch('service.OTPService.check_email')
    @patch('service.OTPService.OTPRepository.addOTP')
    @patch('service.OTPService.sf')
    def test_createOTP_failed_empty_invalid(self,mock_support_function, mock_addOTP, mock_check_email):
        email = "20133"
        mock_support_function.check_email_empty_invalid.return_value = res.ReponseError(status=400, data=res.Message(
            message="Email invalid"))
        request = req.RequestCreateOTP(email=email)
        mock_check_email.return_value = False
        response = createOTP(request)
        self.assertIsInstance(response, res.ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message, "Email invalid")
        mock_addOTP.assert_not_called()

class TestVerifyOTPFunctions(unittest.TestCase):
    @patch('service.OTPService.check_email', return_value=True)
    @patch('service.OTPService.OTPRepository.getOtpByEmail')
    @patch('service.OTPService.OTPRepository.deleteOTP')
    @patch('service.OTPService.sf')
    def test_verifyOTP_success(self,mock_support_function, mock_deleteOTP, mock_getOtpByEmail, mock_check_email):
        current_time = datetime.now()
        mock_support_function.check_email_empty_invalid.return_value = True
        mock_getOtpByEmail.return_value = MagicMock(otp="123456", created_at=current_time - timedelta(minutes=5))

        email = "user@example.com"
        otp = "123456"
        request = req.RequestVerifyOTP(email=email, otp=otp)
        response = verifyOTP(request)
        mock_deleteOTP(email, otp)
        self.assertIsInstance(response, res.ResponseVerifyOTPSignUp)
        self.assertEqual(response.status, 200)
        self.assertEqual(response.data.message, "OTP is valid")

    @patch('service.OTPService.check_email', return_value=True)
    @patch('service.OTPService.OTPRepository.getOtpByEmail')
    @patch('service.OTPService.sf')
    def test_verifyOTP_failed_invalid_otp(self,mock_support_function, mock_getOtpByEmail, mock_check_email):
        current_time = datetime.now()
        mock_support_function.check_email_empty_invalid.return_value = True
        mock_getOtpByEmail.return_value = MagicMock(otp="654321", created_at=current_time - timedelta(minutes=5))

        email = "user@example.com"
        otp = "123456"
        request = req.RequestVerifyOTP(email=email, otp=otp)
        response = verifyOTP(request)
        self.assertIsInstance(response, res.ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message, "Invalid OTP")

    @patch('service.OTPService.check_email')
    @patch('service.OTPService.sf')
    def test_verifyOTP_failed_invalid_email(self,mock_support_function, mock_check_email):
        email = "invalidemail"
        otp = "123456"
        mock_support_function.check_email_empty_invalid.return_value =res.ReponseError(status=400, data=res.Message(
            message="Email invalid"))

        request = req.RequestVerifyOTP(email=email, otp=otp)

        response = verifyOTP(request)
        self.assertIsInstance(response, res.ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message, "Email invalid")

    @patch('service.OTPService.sf')
    def test_verifyOTP_failed_empty_email(self,mock_support_function):
        email = None
        otp = "123456"
        mock_support_function.check_email_empty_invalid.return_value = res.ReponseError(status=400, data=res.Message(
            message="Email is empty"))
        request = req.RequestVerifyOTP(email=email, otp=otp)
        response = verifyOTP(request)
        self.assertIsInstance(response, res.ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message, "Email is empty")

    @patch('service.OTPService.check_email')
    @patch('service.OTPService.sf')
    def test_verifyOTP_failed_empty_otp(self,mock_support_function, mock_check_email):
        email = "user@example.com"
        otp = None
        mock_support_function.check_email_empty_invalid.return_value = True
        request = req.RequestVerifyOTP(email=email, otp=otp)
        mock_check_email.return_value = True
        response = verifyOTP(request)
        self.assertIsInstance(response, res.ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message, "otp is empty")

    @patch('service.OTPService.check_email', return_value=True)
    @patch('service.OTPService.OTPRepository.getOtpByEmail')
    @patch('service.OTPService.sf')
    def test_verifyOTP_failed_no_otp_found(self,mock_support_function, mock_getOtpByEmail, mock_check_email):
        mock_getOtpByEmail.return_value = None
        email = "user@example.com"
        otp = "123456"
        mock_support_function.check_email_empty_invalid.return_value = True
        request = req.RequestVerifyOTP(email=email, otp=otp)
        response = verifyOTP(request)
        self.assertIsInstance(response, res.ReponseError)
        self.assertEqual(response.status, 404)
        self.assertEqual(response.data.message, "No OTP found for this email")

    @patch('service.OTPService.check_email')
    @patch('service.OTPService.OTPRepository.getOtpByEmail')
    @patch('service.OTPService.sf')
    def test_verifyOTP_has_expired(self,mock_support_function, mock_getOtpByEmail, mock_check_email):
        current_time = datetime.now()
        mock_getOtpByEmail.return_value = MagicMock(otp="123456", created_at=current_time - timedelta(minutes=100))
        email = "user@example.com"
        otp = "123456"
        mock_support_function.check_email_empty_invalid.return_value = True
        request = req.RequestVerifyOTP(email=email, otp=otp)
        response = verifyOTP(request)
        self.assertIsInstance(response, res.ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message, "OTP has expired")

class TestVerifyOTPReset(unittest.TestCase):
    @patch('service.OTPService.check_email')
    @patch('service.OTPService.OTPRepository.getOtpByEmail')
    @patch('service.OTPService.OTPRepository')
    @patch('service.OTPService.auth.get_user_by_email')
    @patch('service.OTPService.auth')
    @patch('service.OTPService.sf')
    def test_verifyOTPReset_success(self,mock_support_function, mock_update_user, mock_get_user_by_email, mock_deleteOTP, mock_getOtpByEmail,
                                    mock_check_email):
        current_time = datetime.now()
        mock_support_function.check_email_empty_invalid.return_value = True
        mock_getOtpByEmail.return_value = MagicMock(otp="123456", created_at=current_time - timedelta(minutes=5))
        mock_get_user_by_email.return_value = MagicMock(uid="12345")
        email = "user@example.com"
        otp = "123456"
        mock_check_email.return_value = True
        request = req.RequestVerifyOTP(email=email, otp=otp)
        mock_update_user.update_user(uid="12345", )
        response = verifyOTPReset(request)
        mock_deleteOTP.deleteOTP("user@example.com", "123456")
        self.assertIsInstance(response, res.ResponseVerifyOTP)
        self.assertEqual(response.status, 200)
        self.assertEqual(response.data.message, "New Password send to Email")

    @patch('service.OTPService.check_email')
    @patch('service.OTPService.OTPRepository.getOtpByEmail')
    @patch('service.OTPService.sf')
    def test_verifyOTPReset_failed_invalid_otp(self,mock_support_function, mock_getOtpByEmail, mock_check_email):
        current_time = datetime.now()
        mock_support_function.check_email_empty_invalid.return_value = True
        mock_getOtpByEmail.return_value = MagicMock(otp="654321", created_at=current_time - timedelta(minutes=5))
        email = "user@example.com"
        otp = "123456"
        mock_check_email.return_value = True
        request = req.RequestVerifyOTP(email=email, otp=otp)
        response = verifyOTPReset(request)
        self.assertIsInstance(response, res.ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message, "Invalid OTP")

    @patch('service.OTPService.check_email')
    @patch('service.OTPService.OTPRepository.getOtpByEmail')
    @patch('service.OTPService.sf')
    def test_verifyOTPReset_failed_no_otp_found(self,mock_support_function, mock_getOtpByEmail, mock_check_email):
        mock_getOtpByEmail.return_value = None
        email = "user@example.com"
        otp = "123456"
        request = req.RequestVerifyOTP(email=email, otp=otp)
        mock_support_function.check_email_empty_invalid.return_value = True
        response = verifyOTPReset(request)
        self.assertIsInstance(response, res.ReponseError)
        self.assertEqual(response.status, 404)
        self.assertEqual(response.data.message, "No OTP found for this email")

    @patch('service.OTPService.check_email')
    @patch('service.OTPService.OTPRepository.getOtpByEmail')
    @patch('service.OTPService.sf')
    def test_verifyOTPReset_has_expired(self,mock_support_function, mock_getOtpByEmail, mock_check_email):
        current_time = datetime.now()
        mock_getOtpByEmail.return_value = MagicMock(otp="123456", created_at=current_time - timedelta(minutes=100))
        email = "vonhuy@gmail.com"
        otp = "123456"
        mock_support_function.check_email_empty_invalid.return_value = True
        request = req.RequestVerifyOTP(email=email, otp=otp)
        response = verifyOTPReset(request)
        self.assertIsInstance(response, res.ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message, "OTP has expired")

    @patch('service.OTPService.check_email')
    @patch('service.OTPService.sf')
    def test_verifyOTPReset_failed_invalid_email(self,mock_support_function, mock_check_email):
        email = "invalidemail"
        otp = "123456"
        mock_support_function.check_email_empty_invalid.return_value = res.ReponseError(status=400, data=res.Message(
            message="Email invalid"))
        request = req.RequestVerifyOTP(email=email, otp=otp)
        response = verifyOTPReset(request)
        self.assertIsInstance(response, res.ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message, "Email invalid")

    @patch('service.OTPService.check_email')
    @patch('service.OTPService.OTPRepository.getOtpByEmail')
    @patch('service.OTPService.sf')
    def test_verifyOTPReset_failed_empty_email(self,mock_support_function, mock_getOtpByEmail, mock_check_email):
        email = None
        otp = "123456"
        request = req.RequestVerifyOTP(email=email, otp=otp)
        mock_support_function.check_email_empty_invalid.return_value = res.ReponseError(status=400, data=res.Message(
            message="Email is empty"))
        response = verifyOTPReset(request)
        self.assertIsInstance(response, res.ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message, "Email is empty")

    @patch('service.OTPService.check_email', return_value=True)
    @patch('service.OTPService.sf')
    def test_verifyOTPReset_failed_empty_otp(self,mock_support_function, mock_check_email):
        email = "user@example.com"
        otp = None
        mock_support_function.check_email_empty_invalid.return_value = True
        request = req.RequestVerifyOTP(email=email, otp=otp)
        response = verifyOTPReset(request)
        self.assertIsInstance(response, res.ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message, "OTP is empty")


if __name__ == '__main__':
    unittest.main()
