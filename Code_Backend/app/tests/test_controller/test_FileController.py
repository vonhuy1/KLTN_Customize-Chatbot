import os
import sys
import tempfile
import unittest
from io import BytesIO
from unittest.mock import patch
from fastapi import UploadFile
from fastapi.testclient import TestClient
from response import  ResponseFile as res
from response import  ResponseDefault as res1
app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, app_path)
from controller import FileController
client = TestClient(FileController.router)

@patch('repository.UserRepository.getEmailUserByIdFix')
def test_delete_file_success(mock_user_repo):
    user_id = "1"
    email = 'example@example.com'
    name_file = "test1.pdf"
    mock_user_repo.return_value = (email,)
    response = client.request("DELETE", "/delete_file", json={"user_id": user_id, "name_file": name_file})
    assert response.json()['status'] == 200

@patch('function.support_function.check_email_service')
def test_delete_file_id_not_exist(mock_user_repo):
    user_id = "1"
    email = 'example@example.com'
    name_file = "test1.pdf"
    mock_user_repo.return_value = res1.ReponseError(status=400, data=res.Message(
        message="Id not exist"))
    response = client.request("DELETE", "/delete_file", json={"user_id": user_id, "name_file": name_file})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Id not exist"

@patch('function.support_function.check_email_service')
def test_delete_file_email_empty(mock_user_repo):
    user_id = "1"
    name_file = "test1.pdf"
    mock_user_repo.return_value = res1.ReponseError(status=400, data=res.Message(
        message="Email is empty"))
    response = client.request("DELETE", "/delete_file", json={"user_id": user_id, "name_file": name_file})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Email is empty"

@patch('function.support_function.check_email_service')
def test_delete_file_email_invalid(mock_user_repo):
    user_id = "1"
    email = "20133"
    name_file = "test1.pdf"
    mock_user_repo.return_value = res1.ReponseError(status=400, data=res.Message(
        message="Email invalid"))
    response = client.request("DELETE", "/delete_file", json={"user_id": user_id, "name_file": name_file})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Email invalid"

@patch('function.support_function.check_email_service')
def test_delete_file_namefile_empty(mock_user_repo):
    user_id = "1"
    email = "201333@gmail.com"
    name_file = ""
    mock_user_repo.return_value = (email,)
    response = client.request("DELETE", "/delete_file", json={"user_id": user_id, "name_file": name_file})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Name file is required."

@patch('function.support_function.check_email_service')
def test_delete_all_file_success(mock_user_repo):
    user_id = "1"
    email = "201333@gmail.com"
    mock_user_repo.return_value = (email,)
    response = client.request("DELETE", "/delete", json={"user_id": user_id})
    assert response.json()['status'] == 200
    assert response.json()['data']['message'] == "Delete all file success"

@patch('function.support_function.check_email_service')
def test_delete_all_file_email_empty(mock_user_repo):
    user_id = "1"
    mock_user_repo.return_value = res.ReponseError(status=400, data=res1.Message(
        message="Email is empty"))
    response = client.request("DELETE", "/delete", json={"user_id": user_id})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Email is empty"

@patch('function.support_function.check_email_service')
def test_delete_all_file_email_invalid(mock_user_repo):
    user_id = "1"
    mock_user_repo.return_value = res.ReponseError(status=400, data=res1.Message(
        message="Email invalid"))
    response = client.request("DELETE", "/delete", json={"user_id": user_id})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Email invalid"

@patch('function.support_function.check_email_service')
@patch('service.FileService.sf_dropbox.list_files')
def test_list_name_file_success(mock_list_files, mock_user_repo):
    user_id = "1"
    email = "quangphuc@gmail.com"
    mock_user_repo.return_value = (email,)
    list_files = [
        'demo1.pdf', 'CV_VoNhuY_Java.pdf', 'VanHoangLuong_DangXuanBach_TLCN.docx',
        'THÔNG-TIN-TUYỂN-DỤNG-Java.pdf', 'baitap_qlpv_nhom14.docx', 'PMBOK2012-5rd Edition.pdf',
        'BaoCaoThucTapTotnghiep_20133059_Fpt_Software.docx'
    ]
    mock_list_files.return_value = list_files
    response = client.get("/list_name_files", params={"user_id": user_id})
    assert response.json()['status'] == 200
    assert response.json()['data']['files'] == list_files
    assert len(response.json()['data']['files']) == 7

@patch('function.support_function.check_email_service')
@patch('service.FileService.sf_dropbox.list_files')
def test_list_name_file_id_not_exist(mock_list_files, mock_user_repo):
    user_id = "1"
    email = "quangphuc@gmail.com"
    mock_user_repo.return_value = res1.ReponseError(status=400, data=res.Message(
        message="Id not exist"))
    response = client.get("/list_name_files", params={"user_id": user_id})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Id not exist"

@patch('function.support_function.check_email_service')
@patch('service.FileService.sf_dropbox.list_files')
def test_list_name_file_email_empty(mock_list_files, mock_user_repo):
    user_id = "1"
    email = None
    name_file = "test1.pdf"
    mock_user_repo.return_value = res1.ReponseError(status=400, data=res.Message(
        message="Email is empty"))
    response = client.get("/list_name_files", params={"user_id": user_id})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Email is empty"

@patch('function.support_function.check_email_service')
@patch('service.FileService.sf_dropbox.list_files')
def test_list_name_file_email_invalid(mock_list_files, mock_user_repo):
    user_id = "1"
    email = "20133"
    name_file = "test1.pdf"
    mock_user_repo.return_value = res1.ReponseError(status=400, data=res.Message(
        message="Email invalid"))
    response = client.get("/list_name_files", params={"user_id": user_id})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Email invalid"

@patch('function.support_function.check_email_service')
def test_download_folder_success(mock_user_repo):
    user_id = "1"
    email = 'example@example.com'
    mock_user_repo.return_value = email
    response = client.post("/chatbot/download_folder/", json={"user_id": user_id})
    assert response.json()['status'] == 200
    assert response.json()['data']['message'] == f'Downloaded folder {email} success'

@patch('function.support_function.check_email_service')
def test_download_folder_id_not_exist(mock_user_repo):
    user_id = "1"
    email = 'example@example.com'
    mock_user_repo.return_value = res1.ReponseError(status=400, data=res.Message(
        message="Id not exist"))
    response = client.post("/chatbot/download_folder/", json={"user_id": user_id})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Id not exist"

@patch('function.support_function.check_email_service')
def test_download_folder_email_empty(mock_user_repo):
    user_id = "1"
    email = None
    mock_user_repo.return_value = res1.ReponseError(status=400, data=res.Message(
        message="Email is empty"))
    response = client.post("/chatbot/download_folder/", json={"user_id": user_id})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Email is empty"

@patch('function.support_function.check_email_service')
def test_download_folder_email_invalid(mock_user_repo):
    user_id = "1"
    email = "20133"
    mock_user_repo.return_value = res1.ReponseError(status=400, data=res.Message(
        message="Email invalid"))
    response = client.post("/chatbot/download_folder/", json={"user_id": user_id})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Email invalid"

@patch('function.support_function.check_email_service')
def test_download_file_success(mock_user_repo):
    user_id = "1"
    email = "quangphuc@gmail.com"
    name_file = "demo1.pdf"
    mock_user_repo.return_value = email
    response = client.post("/chatbot/download_files/", json={"user_id": user_id, "name_file": name_file})
    assert response.json()['status'] == 200
    assert response.json()['data']['message'] == f"Downloaded file '{name_file}' by email: '{email}' success"

@patch('function.support_function.check_email_service')
def test_download_file_id_not_exist(mock_user_repo):
    user_id = "1"
    email = "quangphuc@gmail.com"
    name_file = "demo1.pdf"
    mock_user_repo.return_value = res1.ReponseError(status=400, data=res.Message(
        message="Id not exist"))
    response = client.post("/chatbot/download_files/", json={"user_id": user_id, "name_file": name_file})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Id not exist"

@patch('function.support_function.check_email_service')
def test_download_file_email_empty(mock_user_repo):
    user_id = "1"
    email = None
    name_file = "demo1.pdf"
    mock_user_repo.return_value = res1.ReponseError(status=400, data=res.Message(
        message="Email is empty"))
    response = client.post("/chatbot/download_files/", json={"user_id": user_id, "name_file": name_file})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Email is empty"

@patch('function.support_function.check_email_service')
def test_download_file_email_invalid(mock_user_repo):
    user_id = "1"
    email = "quangphuc"
    name_file = "demo1.pdf"
    mock_user_repo.return_value = res1.ReponseError(status=400, data=res.Message(
        message="Email invalid"))
    response = client.post("/chatbot/download_files/", json={"user_id": user_id, "name_file": name_file})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Email invalid"

@patch('function.support_function.check_email_service')
def test_download_file_name_file_empty(mock_user_repo):
    user_id = "1"
    email = "quangphuc@gmail.com"
    name_file = ""
    mock_user_repo.return_value = email
    response = client.post("/chatbot/download_files/", json={"user_id": user_id, "name_file": name_file})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "name_file is empty"

@patch('function.support_function.check_email_service')
def test_upload_files_invalid_email(mock_user_repo):
    user_id = "1"
    mock_user_repo.return_value = res1.ReponseError(status=400, data=res.Message(
        message="Email invalid"))
    data = {
        'user_id': user_id
    }
    response = client.post("/upload_files/", data=data, files=[])
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Email invalid"

@patch('function.support_function.check_email_service')
def test_upload_files_empty_email(mock_user_repo):
    user_id = "1"
    email = None
    mock_user_repo.return_value = res1.ReponseError(status=400, data=res.Message(
        message="Email is empty"))
    data = {
        'user_id': user_id
    }
    response = client.post("/upload_files/", data=data, files=[])
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Email is empty"

@patch('function.support_function.check_email_service')
def test_upload_files_id_not_exist(mock_user_repo):
    user_id = "1"
    email = 'mang1@gmail.com'
    mock_user_repo.return_value = res1.ReponseError(status=400, data=res.Message(
        message="Id not exist"))
    data = {
        'user_id': user_id
    }
    response = client.post("/upload_files/", data=data, files=[])
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Id not exist"

@patch('service.FileService.sf_dropbox.upload_file')
@patch('function.support_function.check_email_service')
@patch('service.FileService.allowed_file')
@patch('service.FileService.check_email')
@patch('service.FileService.os.makedirs')
@patch('builtins.open', new_callable=unittest.mock.mock_open)
def test_upload_files_success(mock_open, mock_makedirs, mock_check_email, mock_allowed_file, mock_get_email_user_by_id,
                              mock_upload_file):
    user_id = "1"
    email = 'mang1@gmail.com'
    mock_get_email_user_by_id.return_value = email
    mock_check_email.return_value = True
    mock_allowed_file.return_value = True

    file_content = b"Test file content"
    file = UploadFile(filename='test.pdf', file=BytesIO(file_content))

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = os.path.join(temp_dir, email)
        os.makedirs(temp_dir_path, exist_ok=True)
        file_path = os.path.join(temp_dir_path, file.filename)
        mock_open.return_value.write.side_effect = lambda content: None if content == file_content else None
        mock_upload_file.side_effect = lambda src, dst: None
        mock_makedirs.side_effect = lambda path, exist_ok: None
        data = {
            'user_id': user_id
        }
        files = {
            'files': (file.filename, file.file, 'application/pdf')
        }
        response = client.post("/upload_files/", data=data, files=files)
        assert response.status_code == 200
        assert response.json()['status'] == 200
        assert response.json()['data']['message'] == "Load file success"
        # expected_src_path = os.path.join(temp_dir_path, file.filename).replace("\\", "/")
        # expected_dst_path = f"/{email}/{file.filename}"
        # actual_src_path, actual_dst_path = mock_upload_file.call_args[0]
        # actual_src_path = actual_src_path.replace("\\", "/")
        # assert expected_src_path == actual_src_path and expected_dst_path == actual_dst_path
@patch('service.FileService.sf_dropbox.upload_file')
@patch('function.support_function.check_email_service')
@patch('service.FileService.allowed_file')
@patch('service.FileService.check_email')
@patch('service.FileService.os.makedirs')
@patch('service.FileService.shutil.copyfileobj')
def test_upload_files_invalid_file_type(mock_copyfileobj, mock_makedirs, mock_check_email, mock_allowed_file,
                                        mock_get_email_user_by_id, mock_upload_file):
    user_id = "1"
    email = 'mang1@gmail.com'
    mock_get_email_user_by_id.return_value = email
    mock_allowed_file.return_value = False
    file_content = b"Test file content"
    file = UploadFile(filename='test.exe', file=BytesIO(file_content))
    data = {
        'user_id': user_id
    }
    files = {
        'files': (file.filename, file.file)
    }
    response = client.post("/upload_files/", data=data, files=files)
    assert response.json()['status'] == 415
    assert response.json()['data']['message'] == "File type not allow"

def test_delete__all_file_user_id_required():
    user_id = None
    response = client.request("DELETE", "/delete", json={"user_id": user_id})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "user_id field is required."

def test_delete_all_file_user_id_is_integer():
    user_id = "aaaa"
    response = client.request("DELETE", "/delete", json={"user_id": "aaaa"})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "user_id must be an integer"

def test_delete_all_file_user_id_is_greater_0():
    response = client.request("DELETE", "/delete", json={"user_id": "0"})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "user_id must be greater than 0"

def test_list_name_files_user_id_required():
    user_id = None
    response = client.request("GET", "/list_name_files/", params ={"user_id": user_id})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "user_id field is required."

def test_list_name_files_user_id_is_integer():
    user_id = "aaaa"
    response = client.request("GET", "/list_name_files/", params={"user_id": user_id})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "user_id must be an integer"

def test_list_name_files_user_id_is_greater_0():
    user_id = "-100"
    response = client.request("GET", "/list_name_files/", params={"user_id": user_id})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "user_id must be greater than 0"

def test_delete_one_file_user_id_required():
    user_id = None
    name_file = "abcd"
    response = client.request("DELETE", "/delete_file/", json ={"user_id": user_id,"name_file": name_file})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "user_id field is required."

def test_delete_one_file_user_id_is_integer():
    user_id = "aaaa"
    name_file = "abcd"
    response = client.request("DELETE", "/delete_file/", json={"user_id": user_id, "name_file": name_file})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "user_id must be an integer"

def test_delete_one_file_user_id_is_greater_0():
    user_id = 0
    name_file = "abcd"
    response = client.request("DELETE", "/delete_file/", json={"user_id": user_id, "name_file": name_file})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "user_id must be greater than 0"

def test_delete_one_file_name_file_required():
    user_id = 1
    name_file = None
    response = client.request("DELETE", "/delete_file/", json ={"user_id": user_id,"name_file": name_file})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Name file is required."

def test_download_folder_user_id_required():
    user_id = None
    response = client.request("POST", "/chatbot/download_folder/", json ={"user_id": user_id})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "user_id field is required."

def test_download_folder_user_id_is_integer():
    user_id = "aaaa"
    response = client.request("POST", "/chatbot/download_folder/", json={"user_id": user_id})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "user_id must be an integer"

def test_download_folder_user_id_is_greater_0():
    user_id = "0"
    response = client.request("POST", "/chatbot/download_folder/", json={"user_id": user_id})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "user_id must be greater than 0"

def test_download_file_user_id_required():
    user_id = None
    response = client.request("POST", "/chatbot/download_files/", json ={"user_id": user_id})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "user_id field is required."

def test_download_files_user_id_is_integer():
    user_id = "aaaa"
    response = client.request("POST", "/chatbot/download_files/", json={"user_id": user_id})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "user_id must be an integer"

def test_download_files_user_id_is_greater_0():
    user_id = "0"
    response = client.request("POST", "/chatbot/download_files/", json={"user_id": user_id})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "user_id must be greater than 0"

def test_upload_file_user_id_required():
    user_id = None
    file_content = b"Test file content"
    file = UploadFile(filename='test.pdf', file=BytesIO(file_content))
    data = {
        'user_id': user_id
    }
    files = {
        'files': (file.filename, file.file)
    }
    response = client.post("/upload_files/", data=data, files=files)
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "user_id field is required."

def test_upload_files_user_id_is_integer():
    user_id = "aaaa"
    file_content = b"Test file content"
    file = UploadFile(filename='test.pdf', file=BytesIO(file_content))
    data = {
        'user_id': user_id
    }
    files = {
        'files': (file.filename, file.file)
    }
    response = client.post("/upload_files/", data=data, files=files)
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "user_id must be an integer"

def test_upload_files_user_id_is_greater_0():
    user_id = "0"
    file_content = b"Test file content"
    file = UploadFile(filename='test.pdf', file=BytesIO(file_content))
    data = {
        'user_id': user_id
    }
    files = {
        'files': (file.filename, file.file)
    }
    response = client.post("/upload_files/", data=data, files=files)
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "user_id must be greater than 0"