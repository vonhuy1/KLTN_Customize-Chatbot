import unittest
import sys
import os
app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, app_path)
from service import UserService
from request import RequestUser as req
from response import ResponseUser as res
from unittest.mock import patch, Mock,MagicMock
from typing import  Optional
from response import ResponseDefault as res1


class TestUpdateUserInfoFunction(unittest.TestCase):
    @patch('service.UserService.UserRepository.getEmailUserByIdFix')
    @patch('service.UserService.check_email')
    @patch('service.UserService.get_user1')
    @patch('service.UserService.UserInfoRepository.getUserInfo')
    @patch('service.UserService.UserInfoRepository.updateUserInfo')
    @patch('service.UserService.UserInfoRepository.addUserInfo')
    @patch('service.UserService.update_info_user')
    @patch('service.UserService.sf.check_email_empty_invalid', return_value=True)
    @patch('service.UserService.sf.check_email_service', return_value="old_email@example.com")
    def test_update_user_info_success_existing_user(self, mock_check1, mock_check2, mock_update_info_user, mock_add_user_info, mock_update_user_info, mock_get_user_info, mock_get_user, mock_check_email, mock_get_email_by_id):
        request = req.RequestUpdateUserInfo(
            user_id = "1",
            email="new_email@example.com",
            uid="uid123",
            display_name="New Name",
            photo_url="http://photo.url"
        )
        mock_get_user.return_value = Mock()  # Simulate user exists
        mock_get_user_info.return_value = Mock()  # Simulate user info exists
        response = UserService.update_user_info(request)
        self.assertEqual(response.status, 200)
        self.assertIsInstance(response, res.ResponseUpdateUserInfo)
        self.assertEqual(response.data.message, "User info updated successfully")
    
    @patch('service.UserService.get_user1')
    @patch('service.UserService.UserInfoRepository.getUserInfo')
    @patch('service.UserService.UserInfoRepository.updateUserInfo')
    @patch('service.UserService.UserInfoRepository.addUserInfo')
    @patch('service.UserService.update_info_user')
    @patch('service.UserService.UserRepository.getEmailUserByIdFix')
    @patch('service.UserService.sf.check_email_empty_invalid', side_effect=Exception("Error"))
    @patch('service.UserService.sf.check_email_service', return_value="old_email@example.com")
    def test_update_user_info_server_error(self,mock_check,mock_check_2,mock_get_email, mock_update_info_user, mock_addUserInfo, mock_updateUserInfo, mock_getUserInfo, mock_get_user1):
        request = MagicMock()
        request.email = 'test@example.com'
        request.user_id = 'test_user_id'
        request.uid = 'test_uid'
        request.display_name = 'Test User'
        request.photo_url = 'https://example.com/photo.jpg'
        response = UserService.update_user_info(request)
        self.assertEqual(response.status, 500)
        self.assertEqual(response.data.message, "Server Error")

    @patch('service.UserService.UserRepository.getEmailUserByIdFix')
    @patch('service.UserService.check_email')
    @patch('service.UserService.get_user1')
    @patch('service.UserService.UserInfoRepository.getUserInfo')
    @patch('service.UserService.UserInfoRepository.updateUserInfo')
    @patch('service.UserService.UserInfoRepository.addUserInfo')
    @patch('service.UserService.update_info_user')
    @patch('service.UserService.sf.check_email_empty_invalid', return_value=True)
    @patch('service.UserService.sf.check_email_service', return_value="old_email@example.com")
    def test_update_user_info_success_new_user_info(self,mock_check1, mock_check2, mock_update_info_user, mock_add_user_info, mock_update_user_info, mock_get_user_info, mock_get_user, mock_check_email, mock_get_email_by_id):
        request = req.RequestUpdateUserInfo(
            user_id = "1",
            email = "new_email@example.com",
            uid="uid123",
            display_name="New Name",
            photo_url="http://photo.url"
        )
        mock_get_user.return_value = Mock()
        mock_get_user_info.return_value = None  
        response = UserService.update_user_info(request)
        self.assertEqual(response.status, 200)
        self.assertIsInstance(response, res.ResponseUpdateUserInfo)
        self.assertEqual(response.data.message, "User info updated successfully")
        mock_update_user_info.assert_not_called()
        mock_add_user_info.assert_called_once()
        mock_update_info_user.assert_called_once()


    @patch('service.UserService.UserRepository.getEmailUserByIdFix')
    @patch('service.UserService.sf.check_email_empty_invalid', return_value=True)
    @patch('service.UserService.sf.check_email_service', return_value= res1.ReponseError(status=400, data=res.Message(
            message="Id not exist")))
    def test_update_user_info_id_not_exist(self, mock_check1,mock_check2,mock_get_email_by_id):
        request = req.RequestUpdateUserInfo(
            user_id= "1",
            email="new_email@example.com",
            uid="uid123",
            display_name="New Name",
            photo_url="http://photo.url"
        )
        response = UserService.update_user_info(request)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message, "Id not exist")
    
    @patch('service.UserService.UserRepository.getEmailUserByIdFix')
    @patch('service.UserService.sf.check_email_empty_invalid', return_value=True)
    @patch('service.UserService.sf.check_email_service', return_value=res1.ReponseError(status=400, data=res.Message(
        message="Email is empty")))
    def test_update_user_info_email_empty(self,mock_check1,mock_check2, mock_get_email_by_id):
        request = req.RequestUpdateUserInfo(
            user_id= "1",
            email=None,
            uid="uid123",
            display_name="New Name",
            photo_url="http://photo.url"
        )
        response = UserService.update_user_info(request)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message, "Email is empty")

    @patch('service.UserService.UserRepository.getEmailUserByIdFix')
    @patch('service.UserService.check_email')
    @patch('service.UserService.sf.check_email_empty_invalid', return_value=True)
    @patch('service.UserService.sf.check_email_service', return_value=res1.ReponseError(status=400, data=res.Message(
        message="Email invalid")))
    def test_update_user_info_email_invalid(self, mock_check1, mock_check2, mock_check_email, mock_get_email_by_id):
        request = req.RequestUpdateUserInfo(
            email="invalid_email",
            user_id= "1",
            uid="uid123",
            display_name="New Name",
            photo_url="http://photo.url"
        )
        response = UserService.update_user_info(request)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message, "Email invalid")

    @patch('service.UserService.UserRepository.getEmailUserByIdFix')
    @patch('service.UserService.check_email')
    @patch('service.UserService.get_user1')
    @patch('service.UserService.sf.check_email_service',return_value="new_email@example.com")
    def test_update_user_info_email_or_password_error(self,mock_check1, mock_get_user, mock_check_email, mock_get_email_by_id):
        request = req.RequestUpdateUserInfo(
            user_id= "1",
            email="new_email@example.com",
            uid="uid123",
            display_name="New Name",
            photo_url="http://photo.url"
        )
        mock_get_user.return_value = None
        response = UserService.update_user_info(request)
        self.assertEqual(response.status, 404)
        self.assertEqual(response.data.message, "Not found user")

class TestCheckInfoGoogle(unittest.TestCase):
    @patch('service.UserService.UserRepository')
    @patch('service.UserService.check_email')
    @patch('service.UserService.UserInfoRepository')
    @patch('service.UserService.sf.check_email_service', return_value="test@gmail.com")
    def test_check_info_google_success(self,mock_check1,mock_user_info_repo,mock_check_email,mock_user_repo):
        user_id = "1"
        email ="test@gmail.com"
        mock_user_info_repo.getUserInfo.return_value = Mock()
        request = req.RequestCheckInfoGoogle(user_id=user_id)
        response = UserService.check_info_google(request)
        self.assertEqual(response.status, 200)
        self.assertEqual(response.data.check, True)
    
    @patch('service.UserService.UserRepository.getEmailUserByIdFix')
    @patch('service.UserService.UserRepository.getEmailUserById')
    @patch('service.UserService.UserInfoRepository.getUserInfo')
    @patch('service.UserService.sf.check_email_service', side_effect = Exception("error"))
    def test_check_info_google_server_error(self,mock_check1, mock_getUserInfo, mock_getEmailUserById, mock_getEmailUserByIdFix):
        mock_getEmailUserByIdFix.side_effect = Exception('Test exception')
        request = MagicMock()
        request.user_id = "1"
        response = UserService.check_info_google(request)
        self.assertEqual(response.status, 500)
        self.assertEqual(response.data.message, "Server Error")

    @patch('service.UserService.UserRepository')
    @patch('service.UserService.check_email')
    @patch('service.UserService.UserInfoRepository')
    @patch('service.UserService.sf.check_email_service', return_value=res.ReponseError(status=400, data=res.Message(
            message="Id not exist")))
    def test_check_info_google_id_not_exist(self,mock_check1, mock_user_info_repo,mock_check_email,mock_user_repo):
        user_id = "1"
        request = req.RequestCheckInfoGoogle(user_id=user_id)
        response = UserService.check_info_google(request)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message, "Id not exist")
    
    @patch('service.UserService.UserRepository')
    @patch('service.UserService.check_email')
    @patch('service.UserService.UserInfoRepository')
    @patch('service.UserService.sf.check_email_service', return_value=res.ReponseError(status=400, data=res.Message(
        message="Email is empty")))
    def test_check_info_google_email_empty(self, mock_check1, mock_user_info_repo, mock_check_email,mock_user_repo):
        user_id = "1"
        email ="quangphuc@gmail.com"
        mock_user_repo.getEmailUserByIdFix.return_value = (email,)
        mock_user_repo.getEmailUserById.return_value = None
        request = req.RequestCheckInfoGoogle(user_id=user_id)
        response = UserService.check_info_google(request)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message, "Email is empty")
    
    @patch('service.UserService.UserRepository')
    @patch('service.UserService.check_email')
    @patch('service.UserService.UserInfoRepository')
    @patch('service.UserService.sf.check_email_service', return_value=res.ReponseError(status=400, data=res.Message(
        message="Email invalid")))
    def test_check_info_google_email_invalid(self,mock_check_1,mock_user_info_repo, mock_check_email,mock_user_repo):
        user_id = "1"
        email ="quangphuc"
        mock_user_repo.getEmailUserByIdFix.return_value = (email,)
        mock_user_repo.getEmailUserById.return_value = (email,)
        mock_check_email.return_value = False
        request = req.RequestCheckInfoGoogle(user_id=user_id)
        response = UserService.check_info_google(request)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message, "Email invalid")
    
class TestCheckInfoGoogleEmail(unittest.TestCase):
    @patch('service.UserService.UserRepository')
    @patch('service.UserService.check_email')
    @patch('service.UserService.UserInfoRepository')
    @patch('service.UserService.sf.check_email_empty_invalid', return_value=True)
    def test_check_info_google_email_success(self,mock_check1, mock_user_info_repo,mock_check_email,mock_user_repo):
        email ="test@gmail.com"
        mock_user_info_repo.getUserInfo.return_value = Mock()
        request = req.RequestCheckInfoGoogleEmail(email=email)
        response = UserService.check_info_google_email(request)
        self.assertEqual(response.status, 200)
        self.assertEqual(response.data.check, True)
    
    @patch('service.UserService.UserInfoRepository.getUserInfoByEmail')
    @patch('service.UserService.sf.check_email_empty_invalid', side_effect=Exception("error"))
    def test_check_info_google_email_server_error(self, mock_check, mock_getUserInfoByEmail):
        request = MagicMock()
        request.email = 'test@example.com'
        response = UserService.check_info_google_email(request)
        self.assertEqual(response.status, 500)
        self.assertEqual(response.data.message, "Server Error")
    
    @patch('service.UserService.UserRepository')
    @patch('service.UserService.check_email')
    @patch('service.UserService.UserInfoRepository')
    @patch('service.UserService.sf.check_email_empty_invalid', return_value=res.ReponseError(status=400, data=res.Message(
            message="Email is empty"))
)
    def test_check_info_google_by_email_email_empty(self,mock_check,mock_user_info_repo,mock_check_email,mock_user_repo):
        email = None
        request = req.RequestCheckInfoGoogleEmail(email=email)
        response = UserService.check_info_google_email(request)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message, "Email is empty")
    
    @patch('service.UserService.UserRepository')
    @patch('service.UserService.check_email')
    @patch('service.UserService.UserInfoRepository')
    @patch('service.UserService.sf.check_email_empty_invalid',
           return_value=res.ReponseError(status=400, data=res.Message(
               message="Email invalid"))
           )
    def test_check_info_google_email_invalid(self,mock_check,mock_user_info_repo,mock_check_email,mock_user_repo):
        email ="quangphuc"
        mock_check_email.return_value = False       
        request = req.RequestCheckInfoGoogleEmail(email=email)
        response = UserService.check_info_google_email(request)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message, "Email invalid")

class TestCheckStateLogin(unittest.TestCase):

    @patch('service.UserService.UserRepository')
    @patch('service.UserService.check_email')
    @patch('service.UserService.UserInfoRepository')
    @patch('service.UserService.get_user1')
    @patch('service.UserService.UserLoginRepository')
    @patch('service.UserService.sf.check_email_service', return_value=True)
    def test_check_state_login_success(self,mock_check,mock_user_login_repo,mock_get_user1,mock_user_info_repo,mock_check_email,mock_user_repo):
        user_id = "1"
        email ="test@gmail.com"
        session_id = "session"
        mock_user_repo.getEmailUserByIdFix.return_value = (email,)
        mock_check_email.return_value = True
        mock_get_user1.return_value = Mock()
        mock_user_login_repo.getUserSessionIdByUserEmail.return_value = session_id
        request = req.RequestCheckStateLogin(user_id=user_id,session_id_now=session_id)
        response = UserService.check_state_login(request)
        self.assertEqual(response.status, 200)
        self.assertEqual(response.data.check, True)
    
    @patch('service.UserService.UserRepository.getEmailUserByIdFix')
    @patch('service.UserService.get_user1')
    @patch('service.UserService.UserLoginRepository.getUserSessionIdByUserEmail')
    @patch('service.UserService.sf.check_email_service', side_effect=Exception("error"))
    def test_check_state_login_server_error(self,mock_check, mock_getUserSessionIdByUserEmail, mock_get_user1, mock_getEmailUserByIdFix):
        request = MagicMock()
        request.user_id = 'test_user_id'
        request.session_id_now = 'test_session_id'
        response = UserService.check_state_login(request)
        self.assertEqual(response.status, 500)
        self.assertEqual(response.data.message, "Server Error")
    

    
    @patch('service.UserService.UserRepository')
    @patch('service.UserService.check_email')
    @patch('service.UserService.UserInfoRepository')
    @patch('service.UserService.get_user1')
    @patch('service.UserService.UserLoginRepository')
    @patch('service.UserService.sf.check_email_service', return_value=res1.ReponseError(status=400, data=res.Message(
        message="Email is empty")))
    def test_check_state_login_email_empty(self, mock_check, mock_user_login_repo,mock_get_user1,mock_user_info_repo,mock_check_email,mock_user_repo):
        user_id = "1"
        email = None
        session_id = "session"
        mock_user_repo.getEmailUserByIdFix.return_value = (email,)
        request = req.RequestCheckStateLogin(user_id=user_id,session_id_now=session_id)
        response = UserService.check_state_login(request)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message, "Email is empty")
    
    @patch('service.UserService.UserRepository')
    @patch('service.UserService.check_email')
    @patch('service.UserService.UserInfoRepository')
    @patch('service.UserService.get_user1')
    @patch('service.UserService.UserLoginRepository')
    @patch('service.UserService.sf.check_email_service', return_value=res1.ReponseError(status=400, data=res.Message(
        message="Email invalid")))
    def test_check_state_login_email_invalid(self,mock_check,mock_user_login_repo,mock_get_user1,mock_user_info_repo,mock_check_email,mock_user_repo):
        user_id = "1"
        email = "20133"
        session_id = "session"
        mock_user_repo.getEmailUserByIdFix.return_value = (email,)
        mock_check_email.return_value = False
        request = req.RequestCheckStateLogin(user_id=user_id,session_id_now=session_id)
        response = UserService.check_state_login(request)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message, "Email invalid")
    
    @patch('service.UserService.UserRepository')
    @patch('service.UserService.check_email')
    @patch('service.UserService.UserInfoRepository')
    @patch('service.UserService.get_user1')
    @patch('service.UserService.UserLoginRepository')
    @patch('service.UserService.sf.check_email_service', return_value=True)
    def test_check_state_session_empty(self,mock_check,mock_user_login_repo,mock_get_user1,mock_user_info_repo,mock_check_email,mock_user_repo):
        user_id = "1"
        email = "20133@gmail.com"
        session_id = None
        request = req.RequestCheckStateLogin(user_id=user_id,session_id_now=session_id)
        response = UserService.check_state_login(request)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message, "session_id is empty")
    
    @patch('service.UserService.UserRepository')
    @patch('service.UserService.check_email')
    @patch('service.UserService.UserInfoRepository')
    @patch('service.UserService.get_user1')
    @patch('service.UserService.UserLoginRepository')
    @patch('service.UserService.sf.check_email_service', return_value=True)
    def test_check_state_login_not_found(self, mock_check, mock_user_login_repo,mock_get_user1,mock_user_info_repo,mock_check_email,mock_user_repo):
        user_id = "1"
        email ="test@gmail.com"
        session_id = "session"
        mock_get_user1.return_value = None
        mock_user_login_repo.getUserSessionIdByUserEmail.return_value = session_id
        request = req.RequestCheckStateLogin(user_id=user_id,session_id_now=session_id)
        response = UserService.check_state_login(request)
        self.assertEqual(response.status, 404)
        self.assertEqual(response.data.message, "Not found user")

class TestChangePassword(unittest.TestCase):

    @patch('service.UserService.UserRepository.getEmailUserByIdFix')
    @patch('service.UserService.check_email')
    @patch('service.UserService.sign_in_with_email_and_password')
    @patch('service.UserService.auth')
    @patch('service.UserService.sf.check_email_service', return_value = "test@example.com")
    def test_change_password_success(self,mock_check, mock_auth, mock_sign_in, mock_check_email, mock_get_email):
        request = req.RequestChangePassword(user_id='123', new_password='new_password', current_password='current_password',confirm_new_password = 'new_password')
        mock_get_email.return_value = ['test@example.com']
        mock_check_email.return_value = True
        mock_sign_in.return_value = MagicMock()
        mock_auth.get_user_by_email.return_value = MagicMock(uid='user_uid')
        response = UserService.change_password(request)
        self.assertEqual(response.status, 200)
        self.assertEqual(response.data.message,"Update password success")
    @patch('service.UserService.UserRepository.getEmailUserByIdFix')
    @patch('service.UserService.sign_in_with_email_and_password')
    @patch('service.UserService.auth.get_user_by_email')
    @patch('service.UserService.auth.update_user')
    @patch('service.UserService.sf.check_email_empty_invalid', side_effect = Exception("error"))
    def test_change_password_server_error(self, mock_check,mock_update_user, mock_get_user_by_email, mock_sign_in_with_email_and_password,mock_get_email):
        request = MagicMock()
        request.user_id = 'test_user_id'
        request.new_password = 'new_password'
        request.current_password = 'current_password'
        request.confirm_new_password='new_password'
        response = UserService.change_password(request)
        self.assertEqual(response.status, 500)
        self.assertEqual(response.data.message, "Server Error!!")
    
    @patch('service.UserService.UserRepository.getEmailUserByIdFix')
    @patch('service.UserService.check_email')
    @patch('service.UserService.sign_in_with_email_and_password')
    @patch('service.UserService.auth')

    @patch('service.UserService.sf.check_email_service', return_value=res1.ReponseError(status=400, data=res.Message(
        message="Id not exist")))
    def test_change_password_id_not_exist(self, mock_check, mock_auth, mock_sign_in, mock_check_email, mock_get_email):
        request = req.RequestChangePassword(user_id='123', new_password='new_password', current_password='current_password',confirm_new_password='new_password')
        mock_get_email.return_value = None
        response = UserService.change_password(request)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message,"Id not exist")
    
    @patch('service.UserService.UserRepository.getEmailUserByIdFix')
    @patch('service.UserService.check_email')
    @patch('service.UserService.sign_in_with_email_and_password')
    @patch('service.UserService.auth')
    @patch('service.UserService.sf.check_email_service', return_value=res1.ReponseError(status=400, data=res.Message(
        message="Email is empty")))
    def test_change_password_email_is_empty(self,mock_check, mock_auth, mock_sign_in, mock_check_email, mock_get_email):
        request = req.RequestChangePassword(user_id='123', new_password='new_password', current_password='current_password',confirm_new_password='new_password')
        mock_get_email.return_value = (None,)
        response = UserService.change_password(request)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message,"Email is empty")
    
    @patch('service.UserService.UserRepository.getEmailUserByIdFix')
    @patch('service.UserService.check_email')
    @patch('service.UserService.sign_in_with_email_and_password')
    @patch('service.UserService.auth')
    @patch('service.UserService.sf.check_email_service', return_value=res1.ReponseError(status=400, data=res.Message(
        message="Email invalid")))
    def test_change_password_email_invalid(self, mock_check,mock_auth, mock_sign_in, mock_check_email, mock_get_email):
        request = req.RequestChangePassword(user_id='123', new_password='new_password', current_password='current_password',confirm_new_password='new_password')
        mock_get_email.return_value = "20133"
        mock_check_email.return_value = False
        response = UserService.change_password(request)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message,"Email invalid")
    
    @patch('service.UserService.UserRepository.getEmailUserByIdFix')
    @patch('service.UserService.check_email')
    @patch('service.UserService.sign_in_with_email_and_password')
    @patch('service.UserService.auth')
    @patch('service.UserService.sf.check_email_service', return_value = True)
    def test_change_password_new_password_empty(self, mock_check, mock_auth, mock_sign_in, mock_check_email, mock_get_email):
        request = req.RequestChangePassword(user_id='123', new_password= None, current_password='current_password',confirm_new_password='new_password')
        mock_get_email.return_value = "20133@gmail.com"
        mock_check_email.return_value = True
        response = UserService.change_password(request)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message,"new_password is empty")

    @patch('service.UserService.UserRepository.getEmailUserByIdFix')
    @patch('service.UserService.check_email')
    @patch('service.UserService.sign_in_with_email_and_password')
    @patch('service.UserService.auth')
    @patch('service.UserService.sf.check_email_service', return_value=True)
    def test_change_password_confirm_new_password_empty(self, mock_check, mock_auth, mock_sign_in, mock_check_email,
                                                mock_get_email):
        request = req.RequestChangePassword(user_id='123', new_password="abc", current_password='current_password',
                                            confirm_new_password=None)
        mock_get_email.return_value = "20133@gmail.com"
        mock_check_email.return_value = True
        response = UserService.change_password(request)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message, "confirm_new_password is empty")

    @patch('service.UserService.UserRepository.getEmailUserByIdFix')
    @patch('service.UserService.check_email')
    @patch('service.UserService.sign_in_with_email_and_password')
    @patch('service.UserService.auth')
    @patch('service.UserService.sf.check_email_service', return_value=True)
    def test_change_password_confirm_new_password_do_not_match_new_password(self, mock_check, mock_auth, mock_sign_in, mock_check_email,
                                                        mock_get_email):
        request = req.RequestChangePassword(user_id='123', new_password="abc", current_password='current_password',
                                            confirm_new_password="ab")
        mock_get_email.return_value = "20133@gmail.com"
        mock_check_email.return_value = True
        response = UserService.change_password(request)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message, "The new_password and the confirm_new_password must be similar")
    
    @patch('service.UserService.UserRepository.getEmailUserByIdFix')
    @patch('service.UserService.check_email')
    @patch('service.UserService.sign_in_with_email_and_password')
    @patch('service.UserService.auth')
    @patch('service.UserService.sf.check_email_service', return_value="test@email.com")
    def test_change_password_current_password_empty(self, mock_check, mock_auth, mock_sign_in, mock_check_email, mock_get_email):
        request = req.RequestChangePassword(user_id='123', new_password= "new_password", current_password=None,confirm_new_password='new_password')
        mock_get_email.return_value = "20133@gmail.com"
        mock_check_email.return_value = True
        response = UserService.change_password(request)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message,"current_password is empty")
    
    @patch('service.UserService.UserRepository.getEmailUserByIdFix')
    @patch('service.UserService.check_email')
    @patch('service.UserService.sign_in_with_email_and_password')
    @patch('service.UserService.auth')
    @patch('service.UserService.sf.check_email_service', return_value="test@email.com")
    def test_change_password_current_password_not_valid(self, mock_check, mock_auth, mock_sign_in, mock_check_email, mock_get_email):
        request = req.RequestChangePassword(user_id='123', new_password='new_password', current_password='current_password', confirm_new_password = 'new_password')
        mock_check_email.return_value = True
        mock_sign_in.return_value = None
        response = UserService.change_password(request)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message,"Current password not valid")

class TestResetPassword(unittest.TestCase):
    @patch('service.UserService.check_email', return_value=True)
    @patch('service.UserService.get_user1', return_value={"email": "user@example.com"})
    @patch('service.UserService.createOTPReset', return_value="123456")
    @patch('service.UserService.sf.check_email_empty_invalid', return_value=True)
    def test_reset_password_success(self, mock_check,mock_createOTPReset, mock_get_user1, mock_check_email):
        request = MagicMock()
        request.email = "user@example.com"
        response = UserService.reset_password(request)
        self.assertEqual(response.status, 200)
        self.assertEqual(response.data.check, True)
        self.assertEqual(response.otp, "123456")

    @patch('service.UserService.sf.check_email_empty_invalid', return_value=res.ReponseError(status=400, data=res.Message(
        message="Email invalid")))

    def test_reset_password_invalid_email(self, mock_check_email):
        request = MagicMock()
        request.email = "invalid_email"
        response = UserService.reset_password(request)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message, "Email invalid")

    @patch('service.UserService.check_email', return_value=True)
    @patch('service.UserService.get_user1', return_value=None)
    @patch('service.UserService.sf.check_email_empty_invalid', return_value=True)
    def test_reset_password_user_not_found(self, mock_check, mock_get_user1, mock_check_email):
        request = MagicMock()
        request.email = "nonexistent@example.com"
        response = UserService.reset_password(request)
        self.assertEqual(response.status, 404)
        self.assertEqual(response.data.message, "Email not exist")
    
    @patch('service.UserService.check_email', return_value=True)
    @patch('service.UserService.get_user1')
    @patch('service.UserService.sf.check_email_empty_invalid', return_value=True)
    def test_reset_password_server_error(self, mock_check, mock_get_user1, mock_check_email):
        request = MagicMock()
        mock_get_user1.side_effect = Exception("Error")
        request.email = "nonexistent@example.com"
        response = UserService.reset_password(request)
        self.assertEqual(response.status, 500)
        self.assertEqual(response.data.message, "Server Error")


if __name__ == '__main__':
    unittest.main()