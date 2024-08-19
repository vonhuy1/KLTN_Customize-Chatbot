import unittest
from unittest.mock import patch
from response import ResponseMySQL as res
import sys
import os
from response import ResponseDefault as res1

app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, app_path)
from models import Database_Entity
from service.MySQLService import edit_chat, delete_chat, render_chat_history, load_chat_history
from request.RequestMySQL import RequestEditNameChat, RequestDeleteChat, RequestRenderChatHistory, \
    RequestLoadChatHistory
from response.ResponseMySQL import ResponseEditChat, ResponseDeleteChat, ReponseError, Message, \
    ResponseRenderChatHistory, UserInfoListResponse, ListUserChat, ResponseLoadChatHistory, ChatDetail, ListChatDeTail


class TestMySQLService(unittest.TestCase):
    @patch('service.MySQLService.UserRepository')
    @patch('service.MySQLService.ChatHistoryRepository')
    @patch('service.MySQLService.sf')
    def test_edit_chat_success(self, mock_support_function, mock_chat_history_repo, mock_user_repo):
        user_id = "1"
        email = 'example@example.com'
        name_old = 'chat123'
        name_new = 'chat1234'
        mock_support_function.check_email_service.return_value = email
        mock_chat_history_repo.getIdChatHistoryByUserIdAndNameChat.return_value = True
        mock_chat_history_repo.getIdChatHistoryByUserIdAndNameChatNew.return_value = None
        request = RequestEditNameChat(user_id=user_id, name_old=name_old, name_new=name_new)
        response = edit_chat(request)
        self.assertIsInstance(response, ResponseEditChat)
        self.assertEqual(response.status, 200)

    @patch('service.MySQLService.UserRepository.getEmailUserByIdFix')
    @patch('service.MySQLService.ChatHistoryRepository')
    @patch('service.MySQLService.sf')
    def test_edit_chat_server_error(self, mock_support_function, mock_chat_history_repo, mock_user_repo):
        user_id = "1"
        email = 'example@example.com'
        name_old = 'chat123'
        name_new = 'chat1234'
        mock_support_function.check_email_service.side_effect = Exception("error")
        request = RequestEditNameChat(user_id=user_id, name_old=name_old, name_new=name_new)
        response = edit_chat(request)
        self.assertIsInstance(response, ReponseError)
        self.assertEqual(response.status, 500)
        self.assertEqual(response.data.message, "Server Error")

    @patch('service.MySQLService.UserRepository')
    @patch('service.MySQLService.ChatHistoryRepository')
    @patch('service.MySQLService.sf')
    def test_edit_chat_id_not_exist(self, mock_support_function, mock_chat_history_repo, mock_user_repo):
        user_id = "1"
        name_old = 'chat123'
        name_new = 'chat1234'
        mock_support_function.check_email_service.return_value = res1.ReponseError(status=400, data=res.Message(
            message="Id not exist"))
        request = RequestEditNameChat(user_id=user_id, name_old=name_old, name_new=name_new)
        response = edit_chat(request)
        self.assertIsInstance(response, res1.ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data, Message(message='Id not exist'))

    @patch('service.MySQLService.UserRepository')
    @patch('service.MySQLService.ChatHistoryRepository')
    @patch('service.MySQLService.sf')
    def test_edit_chat_email_empty(self, mock_support_function, mock_chat_history_repo, mock_user_repo):
        user_id = '1'
        email = ""
        name_old = 'chat123'
        name_new = 'chat1234'
        mock_support_function.check_email_service.return_value = res1.ReponseError(status=400, data=res.Message(
            message="Email is empty"))
        request = RequestEditNameChat(user_id=user_id, name_old=name_old, name_new=name_new)
        response = edit_chat(request)
        self.assertIsInstance(response, res1.ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data, Message(message='Email is empty'))

    @patch('service.MySQLService.UserRepository')
    @patch('service.MySQLService.ChatHistoryRepository')
    @patch('service.MySQLService.sf')
    def test_edit_chat_email_in_valid(self, mock_support_function, mock_chat_history_repo, mock_user_repo):
        user_id = "1"
        email = "20133118"
        name_old = 'chat123'
        name_new = 'chat1234'
        mock_support_function.check_email_service.return_value = res1.ReponseError(status=400, data=res.Message(
            message="Email invalid"))
        request = RequestEditNameChat(user_id=user_id, name_old=name_old, name_new=name_new)
        response = edit_chat(request)
        self.assertIsInstance(response, res1.ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data, Message(message='Email invalid'))

    @patch('service.MySQLService.UserRepository')
    @patch('service.MySQLService.ChatHistoryRepository')
    @patch('service.MySQLService.sf.check_email_service', return_value=True)
    def test_edit_chat_name_old_empty(self, mock_support_function, mock_chat_history_repo, mock_user_repo):
        user_id = "1"
        email = "20133118@gmail.com"
        name_old = ""
        name_new = 'chat1234'
        mock_user_repo.getEmailUserByIdFix.return_value = (email,)
        request = RequestEditNameChat(user_id=user_id, name_old=name_old, name_new=name_new)
        response = edit_chat(request)
        self.assertIsInstance(response, ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data, Message(message='name_old is empty'))

    @patch('service.MySQLService.UserRepository')
    @patch('service.MySQLService.ChatHistoryRepository')
    @patch('service.MySQLService.sf.check_email_service', return_value=True)
    def test_edit_chat_name_new_empty(self, mock_support_function, mock_chat_history_repo, mock_user_repo):
        user_id = "1"
        email = "20133118@gmail.com"
        name_old = 'chat123'
        name_new = ''
        mock_user_repo.getEmailUserByIdFix.return_value = (email,)
        request = RequestEditNameChat(user_id=user_id, name_old=name_old, name_new=name_new)
        response = edit_chat(request)
        self.assertIsInstance(response, ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data, Message(message='name_new is empty'))

    @patch('service.MySQLService.UserRepository')
    @patch('service.MySQLService.ChatHistoryRepository')
    @patch('service.MySQLService.sf.check_email_service', return_value=True)
    def test_edit_chat_update_error(self, mock_support_function, mock_chat_history_repo, mock_user_repo):
        user_id = "1"
        email = "20133118@gmail.com"
        name_old = 'chat123'
        name_new = 'chat1234'
        mock_user_repo.getEmailUserByIdFix.return_value = (email,)
        mock_chat_history_repo.getIdChatHistoryByUserIdAndNameChat.return_value = False
        mock_chat_history_repo.getIdChatHistoryByUserIdAndNameChatNew.return_value = None
        request = RequestEditNameChat(user_id=user_id, name_old=name_old, name_new=name_new)
        response = edit_chat(request)
        self.assertIsInstance(response, ReponseError)
        self.assertEqual(response.status, 500)
        self.assertEqual(response.data, Message(message='Update chat error'))


class TestDeleteChat(unittest.TestCase):
    @patch('service.MySQLService.UserRepository')
    @patch('service.MySQLService.ChatHistoryRepository')
    @patch('service.MySQLService.DetailChatRepository')
    @patch('service.MySQLService.sf.check_email_service', return_value=True)
    def test_delete_chat_success(self, mock_support_function, mock_detail_chat_repo, mock_chat_history_repo,
                                 mock_user_repo):
        user_id = "1"
        email = 'example@example.com'
        chat_name = 'test'
        mock_user_repo.getEmailUserByIdFix.return_value = (email,)
        mock_detail_chat_repo.delete_chat_detail.return_value = True
        mock_chat_history_repo.deleteChatHistory.return_value = True
        request = RequestDeleteChat(user_id=user_id, chat_name=chat_name)
        response = delete_chat(request)
        self.assertIsInstance(response, ResponseDeleteChat)
        self.assertEqual(response.status, 200)

    @patch('service.MySQLService.UserRepository')
    @patch('service.MySQLService.ChatHistoryRepository')
    @patch('service.MySQLService.DetailChatRepository')
    @patch('service.MySQLService.sf.check_email_service', side_effect=Exception("Error"))
    def test_delete_chat_server_error(self, mock_support_function, mock_detail_chat_repo, mock_chat_history_repo,
                                      mock_user_repo):
        user_id = "1"
        email = 'example@example.com'
        chat_name = 'test'

        mock_detail_chat_repo.delete_chat_detail.return_value = True
        mock_chat_history_repo.deleteChatHistory.return_value = True
        request = RequestDeleteChat(user_id=user_id, chat_name=chat_name)
        response = delete_chat(request)
        self.assertIsInstance(response, ResponseDeleteChat)
        self.assertEqual(response.status, 500)

    @patch('service.MySQLService.UserRepository')
    @patch('service.MySQLService.ChatHistoryRepository')
    @patch('service.MySQLService.DetailChatRepository')
    @patch('service.MySQLService.sf.check_email_service', return_value=res1.ReponseError(status=400, data=res.Message(
        message="Id not exist")))
    def test_delete_chat_id_not_exist(self, mock_support_function, mock_detail_chat_repo, mock_chat_history_repo,
                                      mock_user_repo):
        user_id = "1"
        email = 'example@example.com'
        chat_name = 'test'
        mock_user_repo.getEmailUserByIdFix.return_value = None
        request = RequestDeleteChat(user_id=user_id, chat_name=chat_name)
        response = delete_chat(request)
        self.assertIsInstance(response, res1.ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data, Message(message='Id not exist'))

    @patch('service.MySQLService.UserRepository')
    @patch('service.MySQLService.ChatHistoryRepository')
    @patch('service.MySQLService.DetailChatRepository')
    @patch('service.MySQLService.sf.check_email_service', return_value=res1.ReponseError(status=400, data=res.Message(
        message="Email is empty")))
    def test_delete_chat_email_empty(self, mock_support_function, mock_detail_chat_repo, mock_chat_history_repo,
                                     mock_user_repo):
        user_id = "1"
        email = ""
        chat_name = 'test'
        mock_user_repo.getEmailUserByIdFix.return_value = (email,)
        request = RequestDeleteChat(user_id=user_id, chat_name=chat_name)
        response = delete_chat(request)
        self.assertIsInstance(response, res1.ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data, Message(message='Email is empty'))

    @patch('service.MySQLService.UserRepository')
    @patch('service.MySQLService.ChatHistoryRepository')
    @patch('service.MySQLService.DetailChatRepository')
    @patch('service.MySQLService.sf.check_email_service', return_value=res1.ReponseError(status=400, data=res.Message(
        message="Email invalid")))
    def test_delete_chat_email_invalid(self, mock_support_function, mock_detail_chat_repo, mock_chat_history_repo,
                                       mock_user_repo):
        user_id = "1"
        email = "20133118"
        chat_name = 'test'
        mock_user_repo.getEmailUserByIdFix.return_value = (email,)
        request = RequestDeleteChat(user_id=user_id, chat_name=chat_name)
        response = delete_chat(request)
        self.assertIsInstance(response, res1.ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data, Message(message='Email invalid'))

    @patch('service.MySQLService.UserRepository')
    @patch('service.MySQLService.ChatHistoryRepository')
    @patch('service.MySQLService.DetailChatRepository')
    @patch('service.MySQLService.sf.check_email_service', return_value=True)
    def test_delete_chat_chatname_empty(self, mock_support_function, mock_detail_chat_repo, mock_chat_history_repo,
                                        mock_user_repo):
        user_id = "1"
        email = "20133118@gmail.com"
        chat_name = ""
        mock_user_repo.getEmailUserByIdFix.return_value = (email,)
        request = RequestDeleteChat(user_id=user_id, chat_name=chat_name)
        response = delete_chat(request)
        self.assertIsInstance(response, ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data, Message(message='chat_name is empty'))

    @patch('service.MySQLService.UserRepository')
    @patch('service.MySQLService.ChatHistoryRepository')
    @patch('service.MySQLService.DetailChatRepository')
    @patch('service.MySQLService.sf.check_email_service', return_value=True)
    def test_delete_chat_error_1(self, mock_support_function, mock_detail_chat_repo, mock_chat_history_repo,
                                 mock_user_repo):
        user_id = "1"
        email = "20133118@gmail.com"
        chat_name = 'test'
        mock_user_repo.getEmailUserByIdFix.return_value = (email,)
        mock_chat_history_repo.deleteChatHistory.return_value = False
        request = RequestDeleteChat(user_id=user_id, chat_name=chat_name)
        response = delete_chat(request)
        self.assertIsInstance(response, ReponseError)
        self.assertEqual(response.status, 500)
        self.assertEqual(response.data, Message(message='Delete conversation chat error'))


class TestRenderChatHistory(unittest.TestCase):
    @patch('service.MySQLService.UserRepository')
    @patch('service.MySQLService.ChatHistoryRepository')
    @patch('service.MySQLService.sf.check_email_service', return_value=True)
    def test_render_chat_history_success(self, mock_support_function, mock_chat_history_repo, mock_user_repo):
        user_id = "1"
        email = 'example@example.com'
        chat_detail = [Database_Entity.ChatHistory(id=1, email="example@example.com", name_chat="chat1"),
                       Database_Entity.ChatHistory(id=2, email="example@example.com", name_chat="chat2")]
        mock_user_repo.getEmailUserByIdFix.return_value = (email,)
        mock_chat_history_repo.getChatHistoryById.return_value = chat_detail
        request = RequestRenderChatHistory(user_id=user_id)
        response = render_chat_history(request)
        self.assertIsInstance(response, ResponseRenderChatHistory)
        self.assertEqual(response.status, 200)
        self.assertIsInstance(response.data, UserInfoListResponse)
        self.assertEqual(len(response.data.chat), 2)  # Kiểm tra số lượng chat được trả về
        self.assertIsInstance(response.data.chat[0], ListUserChat)

    @patch('service.MySQLService.UserRepository')
    @patch('service.MySQLService.ChatHistoryRepository')
    @patch('service.MySQLService.sf.check_email_service', side_effect=Exception("Error"))
    def test_render_chat_history_server_err(self, mock_support_function, mock_chat_history_repo, mock_user_repo):
        user_id = "1"
        email = 'example@example.com'
        chat_detail = [Database_Entity.ChatHistory(id=1, email="example@example.com", name_chat="chat1"),
                       Database_Entity.ChatHistory(id=2, email="example@example.com", name_chat="chat2")]
        mock_user_repo.getEmailUserByIdFix.side_effect = Exception("error")
        request = RequestRenderChatHistory(user_id=user_id)
        response = render_chat_history(request)
        self.assertIsInstance(response, ReponseError)
        self.assertEqual(response.status, 500)
        self.assertEqual(response.data.message, "Server Error")

    @patch('service.MySQLService.UserRepository')
    @patch('service.MySQLService.ChatHistoryRepository')
    @patch('service.MySQLService.sf.check_email_service', return_value=res1.ReponseError(status=400, data=res.Message(
        message="Id not exist")))
    def test_render_chat_history_id_not_exist(self, mock_support_function, mock_chat_history_repo, mock_user_repo):
        user_id = "1"
        email = 'example@example.com'
        chat_detail = [Database_Entity.ChatHistory(id=1, email="example@example.com", name_chat="chat1"),
                       Database_Entity.ChatHistory(id=2, email="example@example.com", name_chat="chat2")]
        mock_user_repo.getEmailUserByIdFix.return_value = None
        request = RequestRenderChatHistory(user_id=user_id)
        response = render_chat_history(request)
        self.assertIsInstance(response, res1.ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data, Message(message='Id not exist'))

class TestLoadChatHistory(unittest.TestCase):
    @patch('service.MySQLService.DetailChatRepository')
    @patch('service.MySQLService.sf.check_email_service', return_value=True)
    @patch('service.MySQLService.ChatHistoryRepository')
    def test_load_chat_history_success(self, mock_chat_history_repo, mock_support_functon, mock_detail_chat_repo):
        chat_id = "1"
        user_id = "1"
        chat_detail = [Database_Entity.DetailChat(id=1, chat_id=1, YouMessage="question1", AiMessage="AImessage1",
                                                  data_relevant="abc", source_file="abcd"),
                       Database_Entity.DetailChat(id=2, chat_id=1, YouMessage="question2", AiMessage="AImessage2",
                                                  data_relevant="abc", source_file="abcd")]
        mock_chat_history_repo.getChatHistoryByChatIdAndUserId.return_value = True
        mock_detail_chat_repo.getListDetailChatByChatId.return_value = chat_detail
        request = RequestLoadChatHistory(user_id=user_id, chat_id=chat_id)
        response = load_chat_history(request)
        self.assertIsInstance(response, ResponseLoadChatHistory)
        self.assertEqual(response.status, 200)
        self.assertIsInstance(response.data, ListChatDeTail)
        self.assertEqual(len(response.data.detail_chat), 2)
        self.assertIsInstance(response.data.detail_chat[0], ChatDetail)

    @patch('service.MySQLService.DetailChatRepository')
    @patch('service.MySQLService.ChatHistoryRepository', return_value=True)
    @patch('service.MySQLService.sf.check_email_service', side_effect=Exception("Error"))
    def test_load_chat_history_server_err(self, mock_support_function, mock_chat_history_repo, mock_detail_chat_repo):
        chat_id = "1"
        user_id = "1"
        chat_detail = [Database_Entity.DetailChat(id=1, chat_id=1, YouMessage="question1", AiMessage="AImessage1",
                                                  data_relevant="abc", source_file="abcd"),
                       Database_Entity.DetailChat(id=2, chat_id=1, YouMessage="question2", AiMessage="AImessage2",
                                                  data_relevant="abc", source_file="abcd")]
        mock_chat_history_repo.getChatHistoryByChatIdAndUserId.return_value = True
        mock_detail_chat_repo.getListDetailChatByChatId.side_effect = Exception("error")
        request = RequestLoadChatHistory(user_id=user_id, chat_id=chat_id)
        response = load_chat_history(request)
        self.assertIsInstance(response, ReponseError)
        self.assertEqual(response.status, 500)
        self.assertEqual(response.data.message, "Server Error")

    @patch('service.MySQLService.DetailChatRepository')
    @patch('service.MySQLService.sf.check_email_service', return_value="20133118@gmail.com")
    @patch('service.MySQLService.ChatHistoryRepository', return_value=True)
    def test_load_chat_history_error(self, mock_repo1, mock_support_function, mock_detail_chat_repo):
        chat_id = None
        user_id = "1"
        request = RequestLoadChatHistory(user_id=user_id, chat_id=chat_id)
        mock_repo1.getChatHistoryByChatIdAndUserId.return_value = None
        response = load_chat_history(request)
        self.assertIsInstance(response, ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data, Message(message='chat_id is empty'))

    @patch('service.MySQLService.DetailChatRepository')
    @patch('service.MySQLService.sf.check_email_service', return_value="12345@gmail.com")
    @patch('service.MySQLService.ChatHistoryRepository')
    def test_load_chat_history_not_found_chat(self, mock_repo1, mock_support_function, mock_detail_chat_repo):
        chat_id = "1"
        user_id = None
        mock_repo1.getChatHistoryByChatIdAndUserId.return_value = None
        request = RequestLoadChatHistory(user_id=user_id, chat_id=chat_id)
        response = load_chat_history(request)
        self.assertIsInstance(response, ReponseError)
        self.assertEqual(response.status, 404)
        self.assertEqual(response.data, Message(message='Not found chat width chat_id and user_id'))


if __name__ == '__main__':
    unittest.main()