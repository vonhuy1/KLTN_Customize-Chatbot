import os
import sys
from unittest.mock import patch, Mock, MagicMock
from fastapi.testclient import TestClient
app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, app_path)
from controller import UserController
from response import ResponseDefault as res1
client = TestClient(UserController.router)

@patch('function.support_function.check_email_service')
@patch('function.support_function.check_email_empty_invalid', return_value = True)
@patch('service.UserService.check_email')
@patch('service.UserService.get_user1')
@patch('repository.UserInfoRepository.getUserInfo')
@patch('repository.UserInfoRepository.updateUserInfo')
@patch('repository.UserInfoRepository.addUserInfo')
@patch('service.UserService.update_info_user')
def test_update_user_info_success(mock_update_info_user, mock_add_user_info, mock_update_user_info, mock_get_user_info, mock_get_user, mock_check_email, mock_check1, mock_get_email_by_id):
        mock_get_email_by_id.return_value = "old_email@example.com"
        mock_get_user.return_value = Mock()  # Simulate user exists
        mock_get_user_info.return_value = Mock()
        response = client.put("/update_user_info", json={"user_id":1,
                                                          "email": "new_email@example.com",
                                                          "uid":"uid123",
                                                          "display_name":"New Name",
                                                          "photo_url":"http://photo.url"})
        assert response.json()['status'] == 200
        assert response.json() == {
                "status": 200,
                "data": {
                    "message": "User info updated successfully",
                }

            }
from response import  ResponseUser as res
@patch('function.support_function.check_email_service')
@patch('function.support_function.check_email_empty_invalid',return_value = True)
@patch('repository.UserRepository.getEmailUserByIdFix')
def test_update_user_info_id_not_exist(mock_get_email_by_id,mock_check1,mock_check2):
        mock_check2.return_value = res1.ReponseError(status=400, data=res.Message(
        message="Id not exist"))
        response = client.put("/update_user_info", json={"user_id":1,
                                                           "email": "new_email@example.com",
                                                           "uid":"uid123",
                                                           "display_name":"New Name",
                                                           "photo_url":"http://photo.url"})
        assert response.json()['status'] == 400
        assert response.json() == {
                "status": 400,
                "data": {
                    "message": "Id not exist",
                }

            }


def test_update_user_info_email_empty():
        response = client.put("/update_user_info", json={"user_id":1,
                                                          "email": None,
                                                          "uid":"uid123",
                                                          "display_name":"New Name",
                                                          "photo_url":"http://photo.url"})
        assert response.json()['status'] == 400
        assert response.json() == {
                "status": 400,
                "data": {
                    "message": "email field is required.",
                }
            }


@patch('function.support_function.check_email_service', return_value = "20133118@gmail.com")
@patch('service.UserService.sf.check_email_empty_invalid')
def test_update_user_info_email_invalid(mock_check,mock_service):
        mock_check.return_value = res.ReponseError(status=400, data=res.Message(
              message="Email invalid"))
        response = client.put("/update_user_info", json={"user_id":1,
                                                          "email": "20133",
                                                          "uid":"uid123",
                                                          "display_name":"New Name",
                                                          "photo_url":"http://photo.url"})
        assert response.json()['status'] == 400
        assert response.json() == {
                "status": 400,
                "data": {
                    "message": "Email invalid",
                }
            }

@patch('function.support_function.check_email_service', return_value = "20133118@gmail.com")
@patch('service.UserService.sf.check_email_empty_invalid')
@patch('service.UserService.get_user1')
def test_update_user_info_email_or_password_error(mock_get_user, mock_check_email, mock_get_email_by_id):
    mock_get_email_by_id.return_value = "old_email@example.com"
    mock_check_email.return_value = True
    mock_get_user.return_value = None
    response = client.put("/update_user_info", json={"user_id":1,
                                                      "email": "nhuy@gmail.com",
                                                      "uid":"uid123",
                                                      "display_name":"New Name",
                                                      "photo_url":"http://photo.url"})
    assert response.json()['status'] == 404
    assert response.json() == {
                "status": 404,
                "data": {
                    "message": "Not found user",
                }
            } 
@patch('function.support_function.check_email_service', return_value = "20133118@gmail.com")
@patch('service.UserService.check_email')
@patch('repository.UserInfoRepository.getUserInfo')
@patch('repository.UserRepository.getEmailUserByIdFix', return_value = "20133118@gmail.com")
def test_check_info_google_success(mock_check,mock_user_info_repo, mock_check_email,mock_user_repo_email):
    mock_user_info_repo.return_value = Mock()
    user_id = "1"
    response = client.get("/check_info_google", params={"user_id": user_id})
    assert response.json()['status'] == 200
    assert response.json() == {
        "status": 200,
        "data": {
            "check": True,
        }
    }

@patch('function.support_function.check_email_service', return_value = res.ReponseError(status=400, data=res.Message(
        message="Id not exist")))

@patch('repository.UserRepository.getEmailUserByIdFix', return_value = "20133118@gmail.com")
def test_check_info_google_id_not_exist(mock_check1,mock_user_repo):
    user_id = "1"
    response = client.get("/check_info_google", params={"user_id": user_id})
    assert response.json()['status'] == 400
    assert response.json() == {
        "status": 400,
        "data": {
            "message": "Id not exist",
        }
    }


@patch('function.support_function.check_email_service', return_value=res.ReponseError(status=400, data=res.Message(
    message="Email is empty")))

@patch('repository.UserRepository.getEmailUserByIdFix', return_value = "20133118@gmail.com")
def test_check_info_google_email_empty(mock_check1,mock_user_repo_id):
    user_id = "1"
    response = client.get("/check_info_google", params={"user_id": user_id})
    assert response.json()['status'] == 400
    assert response.json() == {
        "status": 400,
        "data": {
            "message": "Email is empty",
        }
    }

@patch('function.support_function.check_email_service', return_value = res.ReponseError(status=400, data=res.Message(
        message="Email invalid")))

@patch('repository.UserRepository.getEmailUserByIdFix', return_value = "20133118@gmail.com")
def test_check_info_google_email_invalid(mock_check_1,mock_user_repo):
    user_id = "1"
    response = client.get("/check_info_google", params={"user_id": user_id})
    assert response.json()['status'] == 400
    assert response.json() == {
        "status": 400,
        "data": {
            "message": "Email invalid",
        }
    }


@patch('service.UserService.sf.check_email_empty_invalid', return_value=True)
@patch('service.UserService.UserInfoRepository')
def test_check_info_google_by_email_success(mock_user_info_repo, mock_check_email):
    email = "test@gmail.com"
    mock_user_info_repo.getUserInfo.return_value = Mock()
    response = client.get("/check_info_google_signup", params={"email": email})
    assert response.json()['status'] == 200
    assert response.json() == {
        "status": 200,
        "data": {
            "check": True,
        }
    }

def test_check_info_google_signup_email_empty():
    email = ""
    response = client.get("/check_info_google_signup", params={"email": None})
    assert response.json()['status'] == 400
    assert response.json() == {
        "status": 400,
        "data": {
            "message": "Email is required.",
        }
    }

def test_check_info_google_signup_email_invalid():
    email ="quangphuc"
    response = client.get("/check_info_google_signup", params={"email": email})
    assert response.json()['status'] == 400
    assert response.json() == {
        "status": 400,
        "data": {
            "message": "Email invalid",
        }
    }
@patch('service.UserService.sf.check_email_service')
@patch('service.UserService.check_email')
@patch('service.UserService.get_user1')
@patch('repository.UserLoginRepository.getUserSessionIdByUserEmail')
def test_check_state_login_success(mock_user_login_repo,mock_get_user1,mock_check_email,mock_user_repo):
        user_id = "1"
        email ="test@gmail.com"
        session_id = "session"
        mock_user_repo.return_value = email
        mock_check_email.return_value = True
        mock_get_user1.return_value = Mock()
        mock_user_login_repo.return_value = session_id
        response = client.get("/check_state_login", params={"user_id": user_id,"session_id_now" :session_id})
        assert response.json()['status'] == 200
        assert response.json() == {
        "status": 200,
        "data": {
            "check": True,
        }
    }

@patch('service.UserService.sf.check_email_service')
def test_check_state_login_id_not_exits(mock_user_repo):
        user_id = "1"
        email ="test@gmail.com"
        session_id = "session"
        mock_user_repo.return_value = res1.ReponseError(status=400, data=res.Message(
        message="Id not exist"))
        response = client.get("/check_state_login", params={"user_id": user_id,
                                                            "session_id_now" :session_id})
        assert response.json()['status'] == 400
        assert response.json() == {
        "status": 400,
        "data": {
            "message": "Id not exist",
        }
        }

@patch('service.UserService.sf.check_email_service')
def test_check_state_login_email_empty(mock_user_repo):
        user_id = "1"
        email =None
        session_id = "session"
        mock_user_repo.return_value = res1.ReponseError(status=400, data=res.Message(
        message="Email is empty"))
        response = client.get("/check_state_login", params={"user_id": user_id,
                                                            "session_id_now" :session_id})
        assert response.json()['status'] == 400
        assert response.json() == {
        "status": 400,
        "data": {
            "message": "Email is empty",
        }
        }

@patch('service.UserService.sf.check_email_service')
@patch('service.UserService.check_email')
def test_check_state_login_email_invalid(mock_check_email,mock_user_repo):
        user_id = "1"
        email = "20133118"
        session_id = "session"
        mock_user_repo.return_value = res1.ReponseError(status=400, data=res.Message(
            message="Email invalid"))
        response = client.get("/check_state_login", params={"user_id": user_id,
                                                            "session_id_now" :session_id})
        assert response.json()['status'] == 400
        assert response.json() == {
        "status": 400,
        "data": {
            "message": "Email invalid",
        }
        }

@patch('service.UserService.sf.check_email_service')
@patch('service.UserService.check_email')
@patch('repository.UserLoginRepository.getUserSessionIdByUserEmail')
def test_check_state_session_empty(mock_user_login_repo,mock_check_email, mock_user_repo):
    user_id = "1"
    email = "20133@gmail.com"
    session_id = None

    mock_user_repo.return_value = email
    mock_user_login_repo.return_value = "some_session_id"

    response = client.get("/check_state_login", params={"user_id": user_id, 
                                                        "session_id_now": session_id})

    assert response.json()['status'] == 400
    assert response.json() == {
        "status": 400,
        "data": {
            "message": "Session Id is required.",
        }
    }

@patch('service.UserService.sf.check_email_service')
@patch('service.UserService.check_email')
@patch('service.UserService.get_user1')
@patch('repository.UserLoginRepository.getUserSessionIdByUserEmail')
def test_check_state_login_not_found(mock_user_login_repo,mock_get_user1,mock_check_email,mock_user_repo):
        user_id = "1"
        email ="test@gmail.com"
        session_id = "session"
        mock_user_repo.return_value = email
        mock_check_email.return_value = True
        mock_get_user1.return_value = None
        mock_user_login_repo.return_value = session_id
        response = client.get("/check_state_login", params={"user_id": user_id,
                                                            "session_id_now" : session_id})
        assert response.json()['status'] == 404
        assert response.json() == {
        "status": 404,
        "data": {
            "message": "Not found user",
            }
        }


       
@patch('service.UserService.sf.check_email_service',return_value= "test@example.com")
@patch('service.UserService.sf.check_email_empty_invalid', return_value=True)
@patch('service.UserService.sign_in_with_email_and_password')
@patch('service.UserService.auth')
def test_change_password_success(mock_auth, mock_sign_in, mock_check_email, mock_get_email):
        user_id='123'
        new_password='new_password'
        current_password='current_password'
        confirm_new_password = 'new_password'
        mock_sign_in.return_value = MagicMock()
        mock_auth.get_user_by_email.return_value = MagicMock(uid='user_uid')
        response = client.put("/change_password", json={"user_id": user_id,
                                                        "new_password" : new_password,
                                                        "current_password": current_password,
                                                        "confirm_new_password": confirm_new_password})
        assert response.json()['status'] == 200
        assert response.json()['data']['message'] == "Update password success"

@patch('service.UserService.sf.check_email_service', return_value=res1.ReponseError(status=400, data=res.Message(
        message="Id not exist")))
def test_change_password_id_not_exist(mock_get_email):
        user_id='123'
        new_password='new_password'
        current_password='current_password'
        confirm_new_password = 'new_password'
        response = client.put("/change_password", json={"user_id": user_id,
                                                        "new_password": new_password,
                                                        "current_password": current_password,
                                                        "confirm_new_password": confirm_new_password})
        assert response.json()['status'] == 400
        assert response.json()['data']['message'] == "Id not exist"

@patch('service.UserService.sf.check_email_service', return_value=res1.ReponseError(status=400, data=res.Message(
        message="Email is empty")))
def test_change_password_email_is_empty(mock_get_email):
        user_id='123'
        new_password='new_password'
        current_password='current_password'
        confirm_new_password = 'new_password'
        response = client.put("/change_password", json={"user_id": user_id,
                                                        "new_password": new_password,
                                                        "current_password": current_password,
                                                        "confirm_new_password": confirm_new_password})
        assert response.json()['status'] == 400
        assert response.json()['data']['message'] == "Email is empty"

@patch('service.UserService.sf.check_email_service', return_value=res1.ReponseError(status=400, data=res.Message(
        message="Email invalid")))
def test_change_password_email_invalid(mock_check_email):
        user_id='123'
        new_password='new_password'
        current_password='current_password'
        confirm_new_password = 'new_password'
        response = client.put("/change_password", json={"user_id": user_id,
                                                        "new_password" : new_password,
                                                        "current_password": current_password,
                                                        "confirm_new_password": confirm_new_password})
        assert response.json()['status'] == 400
        assert response.json()['data']['message'] == "Email invalid"

@patch('service.UserService.sf.check_email_service')
def test_change_password_new_password_empty( mock_get_email):
        user_id='123'
        new_password= None
        current_password='current_password'
        mock_get_email.return_value = "20133@gmail.com"
        confirm_new_password = 'new_password'
        response = client.put("/change_password", json={"user_id": user_id,
                                                        "new_password": new_password,
                                                        "current_password": current_password,
                                                        "confirm_new_password": confirm_new_password})
        assert response.json()['status'] == 400
        assert response.json()['data']['message'] == "New password field is required."

@patch('service.UserService.sf.check_email_service')
def test_change_password_current_password_empty(mock_get_email):
        user_id='123'
        new_password= "new"
        current_password= None
        mock_get_email.return_value = "20133@gmail.com"
        confirm_new_password = 'new_password'
        response = client.put("/change_password", json={"user_id": user_id,
                                                        "new_password": new_password,
                                                        "current_password": current_password,
                                                        "confirm_new_password": confirm_new_password})
        assert response.json()['status'] == 400
        assert response.json()['data']['message'] == "Current password field is required."

@patch('service.UserService.check_email')
@patch('service.UserService.get_user1')
@patch('service.UserService.createOTPReset')
@patch('service.UserService.sf.check_email_empty_invalid', return_value=True)
def test_reset_password_success(mock_check,mock_createOTPReset, mock_get_user1, mock_check_email):
        email = "user@example.com"
        mock_get_user1.return_value = {"email": "user@example.com"}
        mock_createOTPReset.return_value = "123456"
        response = client.post("/reset_password", json={"email": email})
        assert response.json()['status'] == 200
        assert response.json()['data']['check'] == True
        assert response.json()['otp'] == "123456"

def test_reset_password_invalid_email():
        email = "invalid"
        response = client.post("/reset_password", json={"email": email})
        assert response.json()['status'] == 400
        assert response.json()['data']['message'] == "Email invalid"

def test_reset_password_user_not_found():
        email = "nonexistent@example.com"
        response = client.post("/reset_password", json={"email": email})
        assert response.json()['status'] == 404
        assert response.json()['data']['message'] == "Email not exist"

def test_reset_password_email_is_None():
        email = None
        response = client.post("/reset_password", json={"email": email})
        assert response.json()['status'] == 400
        assert response.json()['data']['message'] == "Email is required."



def test_update_user_info_user_id_required():
    email = None
    response = client.put("/update_user_info", json={"user_id": None,
                                                      "email": "new_email@example.com",
                                                      "uid": "uid123",
                                                      "display_name": "New Name",
                                                      "photo_url": "http://photo.url"})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "user_id field is required."

def test_update_user_info_user_id_integer_required():
    response = client.put("/update_user_info", json={"user_id": "aaaa",
                                                      "email": "new_email@example.com",
                                                      "uid": "uid123",
                                                      "display_name": "New Name",
                                                      "photo_url": "http://photo.url"})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "user_id must be an integer"

def test_update_user_info_user_id_greater_than_0():
    response = client.put("/update_user_info", json={"user_id": 0,
                                                      "email": "new_email@example.com",
                                                      "uid": "uid123",
                                                      "display_name": "New Name",
                                                      "photo_url": "http://photo.url"})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "user_id must be greater than 0"

def test_update_user_info_uid_field_required():
    response = client.put("/update_user_info", json={"user_id": 1,
                                                      "email": "new_email@example.com",
                                                      "uid": "",
                                                      "display_name": "New Name",
                                                      "photo_url": "http://photo.url"})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "uid field is required."

def test_update_user_info_email_field_required():
    response = client.put("/update_user_info", json={"user_id": 1,
                                                      "email": None,
                                                      "uid": "aaaa",
                                                      "display_name": "New Name",
                                                      "photo_url": "http://photo.url"})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "email field is required."

def test_update_user_info_dis_play_name_field_required():
    response = client.put("/update_user_info", json={"user_id": 1,
                                                      "email": "test@gmail.com",
                                                      "uid": "aaaa",
                                                      "display_name": "",
                                                      "photo_url": "http://photo.url"})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "display_name field is required."

def test_update_user_info_photo_url_field_required():
    response = client.put("/update_user_info", json={"user_id": 1,
                                                      "email": "test@gmail.com",
                                                      "uid": "aaaa",
                                                      "display_name": "aaaa",
                                                      "photo_url": ""})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "photo_url field is required."

def test_check_info_google_user_id_required():
    user_id = None
    response = client.get("/check_info_google",params={"user_id": user_id})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "user_id field is required."

def test_check_info_google_user_id_must_integer():
    user_id = "aaaa"
    response = client.get("/check_info_google",params={"user_id": user_id})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "user_id must be an integer"

def test_check_info_google_user_id_must_integer_greater_than_0():
    user_id = "0"
    response = client.get("/check_info_google",params={"user_id": user_id})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "user_id must be greater than 0"

def test_check_info_google_sign_up_email_is_required():
    email = None
    response = client.get("/check_info_google_signup", params={"email": email})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Email is required."

def test_check_info_google_sign_up_email_must_str():
    email = "777"
    response = client.get("/check_info_google_signup", params={"email": email})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Email must be a string, not a number."

def test_check_state_login_user_id_required():
   user_id = None
   session_id_now = "abcde"
   response = client.get("/check_state_login", params={"user_id": user_id,"session_id_now":session_id_now})
   assert response.json()['status'] == 400
   assert response.json()['data']['message'] == "user_id field is required."

def test_check_state_login_user_id_must_integer():
    user_id = "aaaa"
    session_id_now = "abcde"
    response = client.get("/check_state_login", params={"user_id": user_id, "session_id_now": session_id_now})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "user_id must be an integer"

def test_check_state_login_user_id_must_integer_greater_than_0():
    user_id = "0"
    session_id_now = "abcde"
    response = client.get("/check_state_login", params={"user_id": user_id, "session_id_now": session_id_now})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "user_id must be greater than 0"

def test_check_state_login_session_id_required():
   user_id = 1
   session_id_now = None
   response = client.get("/check_state_login", params={"user_id": user_id,"session_id_now":session_id_now})
   assert response.json()['status'] == 400
   assert response.json()['data']['message'] == "Session Id is required."

def test_check_state_login_session_id_must_str():
    user_id = 1
    session_id_now = "134"
    response = client.get("/check_state_login", params={"user_id": user_id, "session_id_now": session_id_now})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Session Id must be a string, not a number."


def test_reset_email_required():
   email = None
   response = client.post("/reset_password", json={"email": email})
   assert response.json()['status'] == 400
   assert response.json()['data']['message'] == "Email is required."

def test_reset_email_must_str():
    email = "20133"
    response = client.post("/reset_password", json={"email": email })
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Email must be a string, not a number."

def test_change_password_user_id_required():
    user_id = None
    new_password = "ABC"
    current_password = "abc"
    response = client.put("/change_password", json={"user_id": user_id,
                                                    "new_password": new_password,
                                                    "current_password": current_password})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "user_id field is required."

def test_change_password_user_id_integer():
    user_id = "aaa"
    new_password = "ABC"
    current_password = "abc"
    response = client.put("/change_password", json={"user_id": user_id,
                                                    "new_password": new_password,
                                                    "current_password": current_password})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "user_id must be an integer"

def test_change_password_user_id_integer_greater_than_0():
    user_id = "0"
    new_password = "ABC"
    current_password = "abc"
    confirm_password = "abc"
    response = client.put("/change_password", json={"user_id": user_id,
                                                    "new_password": new_password,
                                                    "current_password": current_password,
                                                    "confirm_new_password": confirm_password})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "user_id must be greater than 0"

def test_change_password_new_password_required():
    user_id = "1"
    new_password = None
    current_password = "abc"
    confirm_password = "abc"
    response = client.put("/change_password", json={"user_id": user_id,
                                                    "new_password": new_password,
                                                    "current_password": current_password,
                                                    "confirm_new_password": confirm_password})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "New password field is required."

def test_change_password_current_password_required():
    user_id = "1"
    new_password = "abc"
    current_password = None
    confirm_password = "abc"
    response = client.put("/change_password", json={"user_id": user_id,
                                                    "new_password": new_password,
                                                    "current_password": current_password,
                                                    "confirm_new_password": confirm_password})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Current password field is required."




