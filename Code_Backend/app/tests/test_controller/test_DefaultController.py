import json
import os
import sys
from unittest.mock import patch, Mock

from fastapi.testclient import TestClient

app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, app_path)
from controller import DefaultController
client = TestClient(DefaultController.router)

def test_create_firebase_user_null_email():
    request_payload = {"email": None}
    response = client.post("/create_firebase_user_google", json=request_payload)
    assert response.json()['status'] == 400
    try:
        response_data = response.json()['data']
        assert response_data['message'] == "Email is required."
    except json.decoder.JSONDecodeError:
        assert response.text == "Email cannot be 'null'."

def test_invalid_email():
    email = "invalid-email"
    token= "token123455"
    response = client.post("/create_firebase_user_google", json={"email": email,"token_google": token})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Email invalid"

@patch('service.DefaultService.sf.check_email_empty_invalid',return_value=True)
@patch('service.DefaultService.get_user')
def test_create_firebase_server_error(mock_get_user, mock_check_email):
    email = "20133118@gmail.com"
    mock_get_user.side_effect = Exception("Unexpected Error")
    token = "token"
    response = client.post("/create_firebase_user_google", json={"email": email, "token_google": token})
    assert response.json()['status'] == 500
    assert response.json()['data']['message'] == "Server Error"

from response import  ResponseDefault as res
@patch('service.DefaultService.sf.check_email_service', return_value=res.ReponseError(status=400, data=res.Message(
        message="Id not exist")))
@patch('service.DefaultService.get_user')
@patch('service.DefaultService.check_email')
def test_id_not_exist(mock_check_email, mock_get_user, mock_getEmailUserByIdFix):
        user_id = "1"
        response = client.get(f"/info_user/{user_id}")
        assert response.json()['status'] == 400
        assert response.json()['data']['message'] == "Id not exist"

@patch('service.DefaultService.sf.check_email_service', return_value=res.ReponseError(status=400, data=res.Message(
        message="Email is empty")))
@patch('service.DefaultService.get_user')
@patch('service.DefaultService.check_email')
def test_info_user_email_empty(mock_check_email, mock_get_user, mock_getEmailUserByIdFix):
        user_id = "1"
        response = client.get(f"/info_user/{user_id}")
        assert response.json()['status'] == 400
        assert response.json()['data']['message'] == "Email is empty"

@patch('service.DefaultService.sf.check_email_service', return_value=res.ReponseError(status=400, data=res.Message(
        message="Email invalid")))
@patch('service.DefaultService.get_user')
@patch('service.DefaultService.check_email')
def test_info_user_email_invalid(mock_check_email, mock_get_user, mock_getEmailUserByIdFix):
        user_id = "1"
        email = "20133118"
        response = client.get(f"/info_user/{user_id}")
        assert response.json()['status'] == 400
        assert response.json()['data']['message'] == "Email invalid"

@patch('service.DefaultService.UserRepository.getEmailUserByIdFix')
@patch('service.DefaultService.get_user', return_value=None)
@patch('service.DefaultService.check_email', return_value=True)
@patch('service.DefaultService.sf.check_email_service',return_value="20133118@gmail.com")
def test_info_user_user_not_found(mock_check,mock_check_email, mock_get_user, mock_getEmailUserByIdFix):
        user_id = "1"
        email = "20133118@gmail.com"
        response = client.get(f"/info_user/{user_id}")
        assert response.json()['status'] == 404
        assert response.json()['data']['message'] == "User not found"

@patch('service.DefaultService.UserRepository.getEmailUserByIdFix')
@patch('service.DefaultService.get_user')
@patch('service.DefaultService.check_email', return_value=True)
@patch('service.DefaultService.sf.check_email_service',return_value="20133118@gmail.com")
def test_info_success(mock_check,mock_check_email, mock_get_user, mock_getEmailUserByIdFix):
        user_id = "1"
        email = "20133118@gmail.com"
        user = Mock()
        user.uid = "12345"
        user.email = "test@example.com"
        user.display_name = "Test User"
        user.photo_url = "http://example.com/photo.jpg"
        mock_get_user.return_value = user
        response = client.get(f"/info_user/{user_id}")
        assert response.json()['status'] == 200
        assert response.json()['data']['uid'] == user.uid
        assert response.json()['data']['email'] == user.email
        assert response.json()['data']['display_name'] == user.display_name
        assert response.json()['data']['photo_url'] == user.photo_url

@patch('service.DefaultService.sf.check_email_service')
@patch('service.DefaultService.get_user')
@patch('service.DefaultService.check_email')
def test_user_info_server_error(mock_check_email, mock_get_user, mock_getEmailUserByIdFix):
        user_id = "1"
        email = "20133118@gmail.com"
        mock_getEmailUserByIdFix.side_effect = Exception("Unexpected Error")
        response = client.get(f"/info_user/{user_id}")
        assert response.json()['status'] == 500
        assert response.json()['data']['message'] ==  "Server Error: Unexpected Error"

@patch('service.DefaultService.check_email_token', return_value=False)
def test_is_me_none_token(mock_check_email_token):
        token = ""
        response = client.get("/is_me/", params={"token": token})
        assert response.json()['status'] == 400
        assert response.json()['data']['message'] == "Token field is required."

@patch('service.DefaultService.check_email_token', return_value=Exception("Error"))
def test_is_me_invalid_token(mock_check_email_token):
        token = "invalid_token"
        response = client.get("/is_me/", params={"token": token})
        assert response.json()['status'] == 500
        assert response.json()['data']['message'] == "Server Error"

@patch('service.DefaultService.UserRepository.getUserByEmail')
@patch('service.DefaultService.check_email_token')
def test_is_me_success(mock_check_email_token, mock_getUserByEmail):
        token = "token"
        mock_check_email_token.return_value = "user@example.com"    
        user = Mock()
        user.id = "1"
        mock_getUserByEmail.return_value = user    
        response = client.get("/is_me/", params={"token": token})
        assert response.json()['status'] == 200
        assert response.json()['data']['user_id'] == 1

@patch('service.DefaultService.check_email_token')
def test_is_me_server_error(mock_check_email_token):
        token = "token"
        mock_check_email_token.side_effect = Exception("Unexpected Error")
        response = client.get("/is_me/", params={"token": token})
        assert response.json()['status'] == 500
        assert response.json()['data']['message'] == "Server Error"

from fastapi import UploadFile
from io import BytesIO
import tempfile, io
@patch('service.DefaultService.sf.check_email_service', return_value=res.ReponseError(status=400, data=res.Message(
        message="Id not exist")))
def test_upload_image_id_not_exist(mock_getUserByEmail):
    user_id = "1"
    file_content = b"test image content"
    file = io.BytesIO(file_content)
    file.name = "test_image.png"

    data = {
        "user_id": user_id,
    }
    files = {"file": ("test_image.png", file, "image/png")}
    response = client.post("/upload_image", data=data, files=files)
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Id not exist"

@patch('service.DefaultService.sf.check_email_service', return_value=res.ReponseError(status=400, data=res.Message(
        message="Email is empty")))
def test_upload_image_email_empty(mock_getUserByEmail):
    user_id = "1"
    file_content = b"test image content"
    file = io.BytesIO(file_content)
    file.name = "test_image.png"

    data = {
        "user_id": user_id,
    }
    files = {"file": ("test_image.png", file, "image/png")}
    response = client.post("/upload_image", data=data, files=files)
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Email is empty"

@patch('service.DefaultService.sf.check_email_service', return_value=res.ReponseError(status=400, data=res.Message(
        message="Email invalid")))
def test_upload_image_email_invalid(mock_getUserByEmail):
    user_id = "1"
    file_content = b"test image content"
    file = io.BytesIO(file_content)
    file.name = "test_image.png"
    data = {
        "user_id": user_id,
    }
    files = {"file": ("test_image.png", file, "image/png")}
    response = client.post("/upload_image", data=data, files=files)
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Email invalid"

@patch('service.DefaultService.sf.check_email_service', return_value="test1333@gmail.com")
@patch('service.DefaultService.cloudinary.uploader.upload')
@patch('service.DefaultService.check_email')
@patch('service.DefaultService.allowed_file')
def test_upload_image_server_err(mock_allowed_file, mock_check_email, mock_upload, mock_get_email):
    mock_check_email.return_value = True
    mock_allowed_file.return_value = False
    user_id = "1"
    file_content = b"test image content"
    file = io.BytesIO(file_content)
    file.name = "test_image.pdf"

    data = {
        "user_id": user_id,
    }
    files = {"file": ("test_image.png", file, "aplication/pdf")}
    response = client.post("/upload_image", data=data, files=files)
    assert response.json()['status'] == 415
    assert response.json()['data']['message'] == "File type not allow"

@patch('service.DefaultService.sf.check_email_service', return_value="test@example.com")
@patch('service.DefaultService.cloudinary.uploader.upload')
@patch('service.DefaultService.check_email')
@patch('service.DefaultService.allowed_file')
def test_upload_image_success(mock_allowed_file, mock_check_email, mock_upload, mock_get_email):
        mock_allowed_file.return_value = True
        mock_upload.return_value = {"secure_url": "https://example.com/image.png"}
        user_id = "1"
        file_content = b"test image content"
        file = io.BytesIO(file_content)
        file.name = "test_image.png"

        data = {
            "user_id": user_id,
        }
        files = {"file": ("test_image.png", file, "image/png")}
        response = client.post("/upload_image", data=data, files=files)
        assert response.json()['status'] == 200
        assert response.json()['data']['url'] == 'https://example.com/image.png'

def test_is_me_token_is_required():
    token = None
    response = client.get("/is_me/",params={'token':token})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Token field is required."

def test_is_me_token_must_be_string():
    token = "013333"
    response = client.get("/is_me/",params={'token':token})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Token must be a string, not a number."

def test_create_firebase_user_google_is_None():
    email = None
    response = client.post("/create_firebase_user_google/",json={'email':email})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Email is required."

def test_create_firebase_user_google_email_must_be_string():
    email = "20133"
    response = client.post("/create_firebase_user_google/",json={'email':email})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Email must be a string, not a number."

def test_create_firebase_user_google_token_is_required():
    email = "abcd@gmail.com"
    response = client.post("/create_firebase_user_google/",json={'email':email,"token_google": None})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Token field is required."

def test_create_firebase_user_google_token_must_be_str():
    email = "abcd@gmail.com"
    response = client.post("/create_firebase_user_google/",json={'email':email,"token_google": "123"})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Token must be a string, not a number."

def test_create_firebase_user_google_token_must_be_str_1():
    email = "abcd@gmail.com"
    response = client.post("/create_firebase_user_google/",json={'email':email,"token_google": 123})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Token must be a string, not a number."





def test_info_user_user_id_must_be_string():
    user_id = "0"
    response = client.get(f"/info_user/{user_id}")
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "user_id must be greater than 0"

def test_upload_image_user_id_integer():
    user_id = "aaaa"
    file_content = b"test image content"
    file = io.BytesIO(file_content)
    file.name = "test_image.png"

    data = {
        "user_id": user_id,
    }
    files = {"file": ("test_image.png", file, "image/png")}
    response = client.post("/upload_image/", data=data, files=files)
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Value must be an integer"

def test_upload_image_user_id_integer():
    user_id = "aaaa"
    file_content = b"test image content"
    file = io.BytesIO(file_content)
    file.name = "test_image.png"

    data = {
        "user_id": user_id,
    }
    files = {"file": ("test_image.png", file, "image/png")}
    response = client.post("/upload_image", data=data, files=files)
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "user_id must be an integer"

def test_upload_image_user_id_greater_than_0():
    user_id = "0"
    file_content = b"test image content"
    file = io.BytesIO(file_content)
    file.name = "test_image.png"

    data = {
        "user_id": user_id,
    }
    files = {"file": ("test_image.png", file, "image/png")}
    response = client.post("/upload_image", data=data, files=files)
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "user_id must be greater than 0"