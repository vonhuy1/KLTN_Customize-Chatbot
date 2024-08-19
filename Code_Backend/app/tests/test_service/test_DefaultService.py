import os
import sys
import unittest
from unittest.mock import patch, Mock,MagicMock
app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, app_path)
from service.DefaultService import *
from request.RequestDefault import *
from response.ResponseDefault import *

class TestCreateFireBaseUser(unittest.TestCase):
    def test_email_none(self):
        request = RequestCreateFireBaseUserGoogle(email=None)
        response = create_firebase_user(request)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message, "Email is empty")
    
    @patch('service.DefaultService.check_email', return_value=False)
    @patch('service.DefaultService.get_user')
    @patch('service.DefaultService.authservice.verify_token_google', return_value=True)
    def test_invalid_email(self,mock_verify, mock_get_user, mock_check_email):
        request = Mock(spec=req.RequestCreateFireBaseUserGoogle)
        request.email = "invalid-email"
        request.token_google = "token"
        response = create_firebase_user(request)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message, "Email invalid")
    
    @patch('service.DefaultService.check_email', return_value=True)
    @patch('service.DefaultService.get_user')
    @patch('service.DefaultService.authservice.verify_token_google',return_value=True)
    def test_existing_user(self,mock_verify, mock_get_user, mock_check_email):
        request = Mock(spec=req.RequestCreateFireBaseUserGoogle)
        request.email = "test@example.com"
        request.token_google = "token"
        user = Mock()
        user.email = "test@example.com"
        user.display_name = "Test User"
        user.uid = "123456"
        user.photo_url = "http://example.com/photo.jpg"
        mock_get_user.return_value = user
        response = create_firebase_user(request)
        self.assertEqual(response.status, 200)
        self.assertEqual(response.data.localId, "123456")
        self.assertEqual(response.data.email, user.email)
        self.assertEqual(response.data.displayName, user.display_name)
        self.assertEqual(response.data.photoUrl, user.photo_url)

    @patch('service.DefaultService.check_email', return_value=True)
    @patch('service.DefaultService.get_user', return_value=None)
    @patch('service.DefaultService.authservice.verify_token_google', return_value=True)
    def test_non_existing_user(self,mock_verify, mock_get_user, mock_check_email):
        request = Mock(spec=req.RequestCreateFireBaseUserGoogle)
        request.email = "test@example.com"
        request.token_google = "token"
        response = create_firebase_user(request)       
        self.assertEqual(response.status, 500)
        self.assertEqual(response.data.message, "Error")

    @patch('service.DefaultService.check_email', return_value=True)
    @patch('service.DefaultService.get_user', return_value=None)
    def test_token_google_empty(self,mock_get_user, mock_check_email):
        request = Mock(spec=req.RequestCreateFireBaseUserGoogle)
        request.email = "test@example.com"
        request.token_google = ""
        response = create_firebase_user(request)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message, "token google not empty")

    @patch('service.DefaultService.check_email', return_value=True)
    @patch('service.DefaultService.get_user', return_value=None)
    def test_token_google_empty(self, mock_get_user, mock_check_email):
        request = Mock(spec=req.RequestCreateFireBaseUserGoogle)
        request.email = "test@example.com"
        request.token_google = ""
        response = create_firebase_user(request)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message, "token google not empty")

    @patch('service.DefaultService.check_email', return_value=True)
    @patch('service.DefaultService.get_user', return_value=None)
    @patch('service.DefaultService.authservice.verify_token_google', return_value=False)
    def test_oauth2_failed(self,mock_verify, mock_get_user, mock_check_email):
        request = Mock(spec=req.RequestCreateFireBaseUserGoogle)
        request.email = "test@example.com"
        request.token_google = "aaaaa"
        response = create_firebase_user(request)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message, "Create user failed")

    @patch('service.DefaultService.sf.check_email_empty_invalid')
    @patch('service.DefaultService.get_user')
    def test_server_error(self, mock_get_user, mock_check_email):
        request = Mock(spec=req.RequestCreateFireBaseUserGoogle)
        request.email = "test@example.com"
        request.token_google ="token"
        #1 of the 2  cases below
        mock_check_email.side_effect = Exception("Unexpected Error")
        # mock_get_user.side_effect = Exception("Unexpected Error")
        response = create_firebase_user(request)
        self.assertEqual(response.status, 500)
        self.assertEqual(response.data.message, "Server Error")

class TestInfoUser(unittest.TestCase):
    @patch('service.DefaultService.UserRepository.getEmailUserByIdFix')
    @patch('service.DefaultService.get_user')
    @patch('service.DefaultService.check_email')
    def test_id_not_exist(self, mock_check_email, mock_get_user, mock_getEmailUserByIdFix):
        request = Mock(spec=req.RequestInfoUser)
        request.user_id = '1'
        mock_getEmailUserByIdFix.return_value = None
        response = info_user(request)
        self.assertEqual(response.status, 404)
        self.assertEqual(response.data.message, "Id not exist")

    @patch('service.DefaultService.UserRepository.getEmailUserByIdFix')
    @patch('service.DefaultService.get_user')
    @patch('service.DefaultService.check_email')
    def test_email_is_none(self, mock_check_email, mock_get_user, mock_getEmailUserByIdFix):
        request = Mock(spec=req.RequestInfoUser)
        request.user_id = '1'
        mock_getEmailUserByIdFix.return_value = [None]
        response = info_user(request)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message, "Email is empty")

    @patch('service.DefaultService.UserRepository.getEmailUserByIdFix')
    @patch('service.DefaultService.get_user')
    @patch('service.DefaultService.check_email', return_value=False)
    def test_invalid_email(self, mock_check_email, mock_get_user, mock_getEmailUserByIdFix):
        request = Mock(spec=req.RequestInfoUser)
        request.user_id = '1'
        mock_getEmailUserByIdFix.return_value = ["invalid-email"]
        response = info_user(request)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message, "Email invalid")

    @patch('service.DefaultService.UserRepository.getEmailUserByIdFix')
    @patch('service.DefaultService.get_user', return_value=None)
    @patch('service.DefaultService.check_email', return_value=True)
    def test_user_not_found(self, mock_check_email, mock_get_user, mock_getEmailUserByIdFix):
        request = Mock(spec=req.RequestInfoUser)
        request.user_id = '1'
        mock_getEmailUserByIdFix.return_value = ["test@example.com"]
        response = info_user(request)
        self.assertEqual(response.status, 404)
        self.assertEqual(response.data.message, "User not found")

    @patch('service.DefaultService.UserRepository.getEmailUserByIdFix')
    @patch('service.DefaultService.get_user')
    @patch('service.DefaultService.check_email', return_value=True)
    def test_successful_user_retrieval(self, mock_check_email, mock_get_user, mock_getEmailUserByIdFix):
        request = Mock(spec=req.RequestInfoUser)
        request.user_id = '1'
        mock_getEmailUserByIdFix.return_value = ["test@example.com"]
        user = Mock()
        user.uid = "12345"
        user.email = "test@example.com"
        user.display_name = "Test User"
        user.photo_url = "http://example.com/photo.jpg"
        mock_get_user.return_value = user
        response = info_user(request)
        self.assertEqual(response.status, 200)
        self.assertEqual(response.data.uid, user.uid)
        self.assertEqual(response.data.email, user.email)
        self.assertEqual(response.data.display_name, user.display_name)
        self.assertEqual(response.data.photo_url, user.photo_url)

    @patch('service.DefaultService.UserRepository.getEmailUserByIdFix')
    @patch('service.DefaultService.get_user')
    @patch('service.DefaultService.check_email')
    @patch('service.DefaultService.sf.check_email_service',side_effect=Exception("Unexpected Error"))
    def test_server_error(self, mock_support_function,mock_check_email, mock_get_user, mock_getEmailUserByIdFix):
        request = Mock(spec=req.RequestInfoUser)
        request.user_id = '1'
        #1 of the 3 cases below
        # mock_get_user.side_effect =  Exception("Unexpected Error")
        # mock_getEmailUserByIdFix.side_effect = Exception("Unexpected Error")
        response = info_user(request)
        self.assertEqual(response.status, 500)
        self.assertIn("Server Error: Unexpected Error", response.data.message)

class TestIsMe(unittest.TestCase):

    @patch('service.DefaultService.check_email_token', return_value=False)
    def test_none_token(self, mock_check_email_token):
        request = Mock(spec=req.RequestIsMe)
        request.token = None
        response = is_me(request)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message, "token is empty")

    @patch('service.DefaultService.check_email_token', return_value=Exception("Error"))
    def test_invalid_token(self, mock_check_email_token):
        request = Mock(spec=req.RequestIsMe)
        request.token = "invalid_token"
        response = is_me(request)   
        self.assertEqual(response.status, 500)
        self.assertEqual(response.data.message, "Server Error")

    @patch('service.DefaultService.UserRepository.getUserByEmail')
    @patch('service.DefaultService.check_email_token')
    def test_valid_token(self, mock_check_email_token, mock_getUserByEmail):
        request = Mock(spec=req.RequestIsMe)
        request.token = "valid_token" 
        mock_check_email_token.return_value = "user@example.com"    
        user = Mock()
        user.id = "1"
        mock_getUserByEmail.return_value = user       
        response = is_me(request)     
        self.assertEqual(response.status, 200)
        self.assertEqual(response.data.user_id, 1)

    @patch('service.DefaultService.check_email_token')
    @patch('service.DefaultService.UserRepository.getUserByEmail')
    def test_server_error(self,mock_user_repo, mock_check_email_token):
        request = Mock(spec=req.RequestIsMe)
        request.token = "some_token"
        #1 of the 2  cases below or all cases
        mock_user_repo.side_effect =  Exception("Unexpected Error")
        # mock_check_email_token.side_effect = Exception("Unexpected Error")
        response = is_me(request)
        self.assertEqual(response.status, 500)
        self.assertIn("Server Error", response.data.message)

import  io
from io import BytesIO
from fastapi import UploadFile
from io import BytesIO
import tempfile
class TestUpLoadFile(unittest.TestCase):
    @patch('service.DefaultService.UserRepository.getEmailUserByIdFix')
    @patch('service.DefaultService.cloudinary.uploader.upload')
    @patch('service.DefaultService.check_email')
    @patch('service.DefaultService.allowed_file')
    def test_upload_image_success(self, mock_allowed_file, mock_check_email, mock_upload, mock_get_email):
        mock_get_email.return_value = ["test@example.com"]
        mock_check_email.return_value = True
        mock_allowed_file.return_value = True
        mock_upload.return_value = {"secure_url": "https://example.com/image.png"}

        file_content = b"test image content"
        file = io.BytesIO(file_content)
        file.name = "test_image.png"

        mock_request = MagicMock()
        mock_request.user_id = 1
        mock_request.files = MagicMock()
        mock_request.files.file = file
        mock_request.files.filename = file.name
        response = upload_image_service(mock_request)

        self.assertIsInstance(response, ResponseUploadImage)
        self.assertEqual(response.status, 200)
        self.assertEqual(response.status, 200)
        self.assertEqual(response.data.url, "https://example.com/image.png")

    @patch('service.DefaultService.UserRepository.getEmailUserByIdFix')
    @patch('service.DefaultService.cloudinary.uploader.upload')
    @patch('service.DefaultService.check_email')
    @patch('service.DefaultService.allowed_file')
    def test_upload_image_invalid_filetype(self, mock_allowed_file, mock_check_email, mock_upload, mock_get_email):
        mock_get_email.return_value = ["test@example.com"]
        mock_check_email.return_value = True
        mock_allowed_file.return_value = False
        mock_upload.return_value = {"secure_url": "https://example.com/image.png"}

        file_content = b"test image content"
        file = io.BytesIO(file_content)
        file.name = "test_image.txt"

        mock_request = MagicMock()
        mock_request.user_id = 1
        mock_request.files = MagicMock()
        mock_request.files.file = file
        mock_request.files.filename = file.name
        response = upload_image_service(mock_request)

        self.assertIsInstance(response, ReponseError)
        self.assertEqual(response.status, 415)
        self.assertEqual(response.data.message, "File type not allow")

    @patch('service.DefaultService.UserRepository.getEmailUserByIdFix')
    @patch('service.DefaultService.cloudinary.uploader.upload')
    @patch('service.DefaultService.check_email')
    @patch('service.DefaultService.allowed_file')
    def test_upload_image_id_not_exist(self, mock_allowed_file, mock_check_email, mock_upload, mock_get_email):
        mock_get_email.return_value = None
        mock_request = MagicMock()
        mock_request.user_id = 1
        mock_request.files = []
        response = upload_image_service(mock_request)

        self.assertIsInstance(response, ReponseError)
        self.assertEqual(response.status, 404)
        self.assertEqual(response.data.message, "Id not exist")

    @patch('service.DefaultService.UserRepository.getEmailUserByIdFix')
    @patch('service.DefaultService.cloudinary.uploader.upload')
    @patch('service.DefaultService.check_email')
    @patch('service.DefaultService.allowed_file')
    def test_upload_image_email_empty(self, mock_allowed_file, mock_check_email, mock_upload, mock_get_email):
        mock_get_email.return_value = (None,)
        mock_request = MagicMock()
        mock_request.user_id = 1
        mock_request.files = []
        response = upload_image_service(mock_request)

        self.assertIsInstance(response, ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message, "Email is empty")

    @patch('service.DefaultService.UserRepository.getEmailUserByIdFix')
    @patch('service.DefaultService.cloudinary.uploader.upload')
    @patch('service.DefaultService.check_email',return_value=False)
    @patch('service.DefaultService.allowed_file')
    def test_upload_image_email_invalid(self, mock_allowed_file, mock_check_email, mock_upload, mock_get_email):
        mock_get_email.return_value = ("20133118",)
        mock_request = MagicMock()
        mock_request.user_id = 1
        mock_request.files = []
        response = upload_image_service(mock_request)

        self.assertIsInstance(response, ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message, "Email invalid")

    @patch('service.DefaultService.UserRepository.getEmailUserByIdFix')
    @patch('service.DefaultService.cloudinary.uploader.upload')
    @patch('service.DefaultService.check_email', return_value=False)
    @patch('service.DefaultService.allowed_file')
    def test_upload_image_server_err(self, mock_allowed_file, mock_check_email, mock_upload, mock_get_email):
        mock_get_email.side_effect = Exception("Unexpected Error")
        mock_request = MagicMock()
        mock_request.user_id = 1
        mock_request.files = []
        response = upload_image_service(mock_request)

        self.assertIsInstance(response, ReponseError)
        self.assertEqual(response.status, 500)
        self.assertEqual(response.data.message, "Server Error")

if __name__ == '__main__':
    unittest.main()