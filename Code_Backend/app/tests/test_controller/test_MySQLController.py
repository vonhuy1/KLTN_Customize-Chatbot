import os
import sys
from unittest.mock import patch

from fastapi.testclient import TestClient

app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, app_path)
from controller import MySQLController
from models import Database_Entity
from response import ResponseMySQL as res
client = TestClient(MySQLController.router)

def test_render_chat_history():
    with patch('repository.UserRepository.getEmailUserByIdFix') as mock_get_email_user_by_id:
        mock_get_email_user_by_id.return_value = ("example@example.com",)
        with patch('repository.ChatHistoryRepository.getChatHistoryById') as mock_get_chat_history_by_id:
            mock_get_chat_history_by_id.return_value = [Database_Entity.ChatHistory(id = 1,
                                                                                    email = "example@example.com",
                                                                                    name_chat = "chat1") ]
            response = client.get("/chat_history/1")
            assert response.status_code == 200
            assert response.json() == {
                "status": 200,
                "data": {
                    "chat": [
                        {
                            "id": 1,
                            "email": "example@example.com",
                            "chat_name": "chat1"
                        }
                    ]
                }
            }
@patch('repository.ChatHistoryRepository.getChatHistoryByChatIdAndUserId', return_value = True)
@patch('repository.UserRepository.getEmailUserByIdFix', return_value = "20133118@gmail.com")
@patch('function.support_function.check_email_service', return_value = "20133118@gmail.com")
def test_load_chat_history(mock3,mokc1,mock_check_exist):
    with patch('repository.DetailChatRepository.getListDetailChatByChatId') as mock_get_list_detail_chat_by_chat_id:
        mock_get_list_detail_chat_by_chat_id.return_value = [Database_Entity.DetailChat(id=1, chat_id=1,
                                                                                        YouMessage="question1",
                                                                                        AiMessage="AImessage1",
                                                                                        data_relevant="abcd",
                                                                                        source_file="/demo1.pdf")]
        response = client.get("/detail_chat/1/1")
        assert response.status_code == 200
        assert response.json() == {
            "status": 200,
            "data": {
                "detail_chat": [
                    {
                        "id": 1,
                        "chat_id": 1,
                        "question": "question1",
                        "answer": "AImessage1",
                        'data_relevant': 'abcd',
                        'source_file': '/demo1.pdf'
                    }
                ]
            }
        }

def test_load_chat_history_user_id_must_be_integer():
     response = client.get("/detail_chat/aaaa/1")
     assert response.json()['status'] == 400
     assert response.json() == {
        "status": 400,
        "data": {
            "message": "user_id must be an integer"
        }
    }

def test_load_chat_history_user_id_greater_than0():
     response = client.get("/detail_chat/0/1")
     assert response.json()['status'] == 400
     assert response.json() == {
        "status": 400,
        "data": {
            "message": "user_id must be greater than 0"
        }
    }

def test_edit_chat_success():
    with patch('service.MySQLService.edit_chat') as mock_edit_chat:
        mock_edit_chat.return_value = res.ResponseEditChat(status=200, data=res.Message(message="Edit chat success"))
        response = client.put("/edit_chat/", json={"user_id": 1, "name_old": "old_name", "name_new": "new_name"})
        assert response.status_code == 200
        assert response.json() == {
            "status": 200,
            "data": {
                "message": "Edit chat success"
            }
        }

@patch('service.MySQLService.edit_chat')
def test_edit_chat_invalid_id(mock_edit_chat):
    with patch('repository.UserRepository.getEmailUserByIdFix') as mock_get_email_user_by_id:
        mock_get_email_user_by_id.return_value = None
        mock_edit_chat.return_value = res.ReponseError(status= 400, data=res.Message(message="Id not exist"))
        response = client.put("/edit_chat/", json={"user_id": 1, "name_old": "old_name", "name_new": "new_name"})
        assert response.json()['status'] == 400
        assert response.json() == {
            "status": 400,
            "data": {
                "message": "Id not exist"
            }
        }

@patch('repository.UserRepository.getEmailUserByIdFix')
@patch('service.MySQLService.edit_chat')
def test_edit_chat_email_empty(mock_edit_chat,mock_get_email_user_by_id):
    email = ""
    mock_get_email_user_by_id.return_value = (email,)
    mock_edit_chat.return_value = res.ReponseError(status= 400, data=res.Message(message="Email is empty"))
    response = client.put("/edit_chat/", json={"user_id": 1, "name_old": "old_name", "name_new": "new_name"})
    assert response.json()['status'] == 400
    assert response.json() == {
        "status": 400,
        "data": {
            "message": "Email is empty"
        }
    }

@patch('repository.UserRepository.getEmailUserByIdFix')
@patch('service.MySQLService.edit_chat')
def test_edit_chat_email_invalid(mock_edit_chat,mock_get_email_user_by_id):
    email = "20133118"
    mock_get_email_user_by_id.return_value = (email,)
    mock_edit_chat.return_value = res.ReponseError(status= 400, data=res.Message(message="Email invalid"))
    response = client.put("/edit_chat/", json={"user_id": 1, "name_old": "old_name", "name_new": "new_name"})
    assert response.json()['status'] == 400
    assert response.json() == {
        "status": 400,
        "data": {
            "message": "Email invalid"
        }
    }

@patch('repository.UserRepository.getEmailUserByIdFix')
@patch('service.MySQLService.edit_chat')
def test_edit_chat_name_old(mock_edit_chat,mock_get_email_user_by_id):
    email = "20133118@gmail.com"
    mock_get_email_user_by_id.return_value = (email,)
    mock_edit_chat.return_value = res.ReponseError(status= 400, data=res.Message(message="Name old is empty"))
    response = client.put("/edit_chat/", json={"user_id": 1, "name_old": "", "name_new": "new_name"})
    assert response.json()['status'] == 400
    assert response.json() == {
        "status": 400,
        "data": {
            "message": "Name old is empty"
        }
    }

@patch('repository.UserRepository.getEmailUserByIdFix')
@patch('service.MySQLService.edit_chat')
def test_edit_chat_name_new(mock_edit_chat,mock_get_email_user_by_id):
    email = "20133118@gmail.com"
    mock_get_email_user_by_id.return_value = (email,)
    mock_edit_chat.return_value = res.ReponseError(status= 400, data=res.Message(message="Name new is empty"))
    response = client.put("/edit_chat", json={"user_id": 1, "name_old": "123", "name_new": ""})
    assert response.json()['status'] == 400
    assert response.json() == {
        "status": 400,
        "data": {
            "message": "Name new is empty"
        }
    }

@patch('repository.ChatHistoryRepository.getIdChatHistoryByUserIdAndNameChat')
@patch('repository.UserRepository.getEmailUserByIdFix')
@patch('service.MySQLService.edit_chat')
def test_edit_chat1_error(mock_edit_chat,mock_get_email_user_by_id,mock_get_chat_id):
    email = "20133118@gmail.com"
    mock_get_email_user_by_id.return_value = (email,)
    mock_get_chat_id.return_value = False
    mock_edit_chat.return_value = res.ReponseError(status=500,data= res.Message(message="Update chat name error"))
    response = client.put("/edit_chat/", json={"user_id": 1, "name_old": "123", "name_new": "1234"})
    assert response.json()['status'] == 500
    assert response.json() == {
        "status": 500,
        "data": {
            "message": "Update chat name error"
        }
    }

def test_delete_chat_success():
    with patch('service.MySQLService.delete_chat') as mock_delete_chat:
        mock_delete_chat.return_value = res.ResponseDeleteChat(status=200, data=res.Message(message="Delete chat success"))
        response = client.request("DELETE", "/chat_history/delete", json={"user_id": 1, "chat_name": "chat_name"})
        assert response.status_code == 200
        assert response.json() == {
            "status": 200,
            "data": {
                "message": "Delete chat success"
            }
        }

@patch('service.MySQLService.delete_chat')
def test_delete_chat_id_not_exits(mock_delete_chat):
    with patch('repository.UserRepository.getEmailUserByIdFix') as mock_get_email_user_by_id:
        mock_get_email_user_by_id.return_value = None
        mock_delete_chat.return_value = res.ReponseError(status= 400, data=res.Message(message="Id not exist"))
        response = client.request("DELETE", "/chat_history/delete", json={"user_id": 1, "chat_name": "chat_name"})
        assert response.json()['status']== 400
        assert response.json() == {
            "status": 400,
            "data": {
                "message": "Id not exist"
            }
        }

@patch('repository.UserRepository.getEmailUserByIdFix')
@patch('service.MySQLService.delete_chat')
def test_delete_chat_email_empty(mock_delete_chat,mock_get_email_user_by_id):
    email = ""
    mock_get_email_user_by_id.return_value = (email,)
    mock_delete_chat.return_value = res.ResponseDeleteChat(status=400, data=res.Message(message="Email is empty"))
    response = client.request("DELETE", "/chat_history/delete", json={"user_id": 1, "chat_name": "chat_name"})
    assert response.json()['status'] == 400
    assert response.json() == {
        "status": 400,
        "data": {
            "message": "Email is empty"
        }
    }

@patch('repository.UserRepository.getEmailUserByIdFix')
@patch('service.MySQLService.delete_chat')
def test_delete_chat_email_invalid(mock_delete_chat,mock_get_email_user_by_id):
    email = "20133118"
    mock_get_email_user_by_id.return_value = (email,)
    mock_delete_chat.return_value = res.ReponseError(status= 400, data=res.Message(message="Email invalid"))
    response = client.request("DELETE", "/chat_history/delete", json={"user_id": 1, "chat_name": "chat_name"})
    assert response.json()['status'] == 400
    assert response.json() == {
        "status": 400,
        "data": {
            "message": "Email invalid"
        }
    }

@patch('repository.UserRepository.getEmailUserByIdFix')
@patch('service.MySQLService.delete_chat')
def test_delete_chat_name_empty(mock_delete_chat,mock_get_email_user_by_id):
    email = "20133118@gmail.com"
    mock_get_email_user_by_id.return_value = (email,)
    mock_delete_chat.return_value = res.ReponseError(status= 400, data=res.Message(message="Chat name is empty"))
    response = client.request("DELETE", "/chat_history/delete", json={"user_id": 1, "chat_name": ""})
    assert response.json()['status'] == 400
    assert response.json() == {
        "status": 400,
        "data": {
            "message": "Chat name is empty"
        }
    }

@patch('repository.UserRepository.getEmailUserByIdFix')
@patch('repository.ChatHistoryRepository.deleteChatHistory')
@patch('service.MySQLService.delete_chat')
def test_delete_chat_name_error_500(mock_delete_chat,mock_chat_history_repo,mock_get_email_user_by_id):
    email = "20133118@gmail.com"
    mock_get_email_user_by_id.return_value = (email,)
    mock_chat_history_repo.return_value = False
    mock_delete_chat.return_value = res.ResponseDeleteChat(status=500, data=res.Message(message="Delete chat error"))
    response = client.request("DELETE", "/chat_history/delete", json={"user_id": 1, "chat_name": "1234"})
    assert response.json()['status'] == 500
    assert response.json() == {
        "status": 500,
        "data": {
            "message": "Delete chat error"
        }
    }

def test_render_chat_value_mustbe_interger():
    user_id = "aaaa"
    response = client.get(f"/chat_history/{user_id}")
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "user_id must be an integer"

def test_render_chat_user_id_greater_than_inter():
    user_id = "0"
    response = client.get(f"/chat_history/{user_id}")
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "user_id must be greater than 0"


def test_load_chat_history_chat_id_greater_than_inter():
    chat_id = "0"
    user_id = 1
    response = client.get(f"/detail_chat/{user_id}/{chat_id}")
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Value must be greater than 0"

def test_load_chat_history_value_mustbe_inter():
    chat_id = "aaaa"
    user_id = 1
    response = client.get(f"/detail_chat/{user_id}/{chat_id}")
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Value must be an integer"


def test_load_chat_history_user_id_greater_than_inter():
    chat_id = "1"
    user_id = 0
    response = client.get(f"/detail_chat/{user_id}/{chat_id}")
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "user_id must be greater than 0"

def test_load_chat_history_user_id_mustbe_inter():
    chat_id = "1"
    user_id = "aaaaa"
    response = client.get(f"/detail_chat/{user_id}/{chat_id}")
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "user_id must be an integer"
