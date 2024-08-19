import os
import sys
from unittest.mock import patch
from fastapi import  Path
from fastapi.testclient import TestClient
app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, app_path)
from controller import ChatController
import json
client = TestClient(ChatController.router)

text_all = [{
                "page_content": "Thành lập vào năm 2012, VMO Holdings (VMO) là công ty cung cấp dịch vụ CNTT chuyên nghiệp có trụ sở tại Việt Nam, Nhật Bản, Thái Lan và Mỹ. Với hơn 10 năm hoạt động trong lĩnh vực tư vấn và phát triển phần mềm, VMO hiện có hơn 1200 nhân sự và 9 văn phòng tại Việt Nam.\n\nHoàn thiện hệ sinh thái VMO và hướng tới giá trị cốt lõi trong tất cả các hoạt động, VMO tự tin trao quyền và niềm tin cho thế hệ kế cận. Chúng tôi luôn sẵn sàng chào đón các nhân tài cùng tham gia chinh phục thử thách trên những chặng đường sắp tới.\n\nTìm hiểu thêm về VMO Holdings qua:\n\n LinkedIn  Facebook  Website\n\nTHÔNG TIN TUYỂN DỤNG\n\nVị trí:\n\nĐịa điểm:\n\nBusiness Development Intern\n\nHà Nội\n\nKinh nghiệm:\n\nSố lượng:\n\nKhông yêu cầu kinh nghiệm 12\n\nMỨC HỖ TRỢ\n\nUpto 3M (Tùy theo năng lực) + Thưởng hoa hồng\n\nMÔ TẢ CÔNG VIỆC\n\nTham gia chương trình đào tạo miễn phí trong vòng 3 tháng theo lộ trình được\n\nxây dựng bài bản của công ty\n\nTham gia đào tạo các kỹ năng mềm, quy trình làm việc chuyên nghiệp  Trải nghiệm thực tế các công việc của một Business Developer như: + Tìm kiếm và kết nối với khách hàng + Giới thiệu sơ bộ về sản phẩm và dịch vụ công ty với khách hàng + Khai thác dữ liệu khách hàng\n\n[Type here]\n\nYÊU CẦU CÔNG VIỆC\n\nSử dụng Tiếng Anh thành thạo\n\nChăm chỉ, kiên nhẫn  Năng động, cởi mở, hòa đồng \n\nThông minh, tiếp thu nhanh, tư duy nhạy bén\n\nCó tinh thần cầu tiến trong công việc  Có kỹ năng giao tiếp và giải quyết vấn đề tốt  Có khả năng làm việc nhóm tốt  Đảm bảo làm việc full-time sau quá trình đào tạo\n\nQUYỀN LỢI\n\nCó cơ hội trở thành nhân viên chính thức tại VMO sau quá trình đào tạo   Được học tập với đội ngũ Mentors là Sales Manager, Teamlead có nhiều kinh nghiệm trong ngành Sales IT Global\n\nĐược tham gia các chương trình đào tạo nâng cao kỹ năng chuyên môn định kỳ\n\nhàng tháng\n\nĐược làm việc trực tiếp với khách hàng đa quốc gia thuộc nhiều lĩnh vực khác\n\nnhau\n\nĐược đào tạo trong môi trường năng động, trẻ trung, hiện đại và chuyên nghiệp\n\nCƠ HỘI VÀ THỬ THÁCH\n\nCơ hội được thử sức với các dự án hấp dẫn, thử thách đủ lớn trong và ngoài nước.  Cơ hội làm trải nghiệm môi trường làm việc cởi mở và năng động, khuyến khích trao đổi ý tưởng, trao quyền, cho phép làm việc, sáng tạo theo cách riêng. Tài năng và thành tích của từng nhân viên được trân trọng, nhân viên xuất sắc được khen thưởng hàng năm.\n\nCơ hội phát triển năng lực, được hỗ trợ phụ cấp chứng chỉ chuyên môn phục vụ công việc. Một số chứng chỉ cấp cao sẽ được chi trả toàn bộ chi phí từ học và thi.  Dự án khủng với domain hot-trend, liên tục cập nhật những công nghệ mới nhất Được làm việc trong môi trường có quy trình chuyên nghiệp, cùng những chuyên gia công nghệ đến từ các nước và khu vực khác nhau\n\n[Type here]\n\nVui lòng gửi CV của bạn về địa chỉ email: minhdn4@vmogroup.com\n\nEmail: minhdn4@vmogroup.com\n\nĐịa chỉ: Phòng Tuyển dụng – VMO Holdings, Tầng 20, Tòa IDMC, Số 18 Tôn Thất Thuyết, Mỹ Đình, Hà Nội.\n\n[Type here]",
                "metadata": {"source": "/code/temp/vonhuytest123456789@gmail.com/JD_BD-Intern.pdf"},
                "type": "Document"}]

from response import  ResponseChat as res
@patch('function.support_function.check_email_service')
def test_query2_upgrade_old_id_not_exist(mock_user_repo):
    mock_user_repo.return_value = res.ReponseError(status=400, data=res.Message(
        message="Id not exist"))
    response = client.post("/chatbot/query/", data={"user_id": 1,
                                                    "text_all": json.dumps(text_all),
                                                    "question": "12455",
                                                    "chat_name": "test"})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Id not exist"

@patch('function.support_function.check_email_service')
def test_query2_upgrade_old_email_empty(mock_user_repo):
    mock_user_repo.return_value = res.ReponseError(status=400, data=res.Message(
        message="Email is empty"))
    response = client.post("/chatbot/query/", data={"user_id": 1,
                                                    "text_all": json.dumps(text_all),
                                                    "question": "12455",
                                                    "chat_name": "test"})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Email is empty"

@patch('function.support_function.check_email_service')
def test_query2_upgrade_old_email_in_valid(mock_user_repo):
    mock_user_repo.return_value = res.ReponseError(status=400, data=res.Message(
        message="Email invalid"))
    response = client.post("/chatbot/query/", data={"user_id": 1,
                                                    "text_all": json.dumps(text_all),
                                                    "question": "12455",
                                                    "chat_name": "test"})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Email invalid"

@patch('function.support_function.check_email_service')
def test_query2_upgrade_old_question_empty(mock_user_repo):
    mock_user_repo.return_value = "example@example.com"
    response = client.post("/chatbot/query/", data={"user_id": 1,
                                                    "text_all": json.dumps(text_all),
                                                    "question": "",
                                                    "chat_name": "test"})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "question is empty"

@patch('function.support_function.check_email_service')
def test_query2_upgrade_old_chat_history_empty(mock_user_repo):
    mock_user_repo.return_value = "example@example.com"
    response = client.post("/chatbot/query/", data={"user_id": 1,
                                                    "text_all": json.dumps(text_all),
                                                    "question": "123",
                                                    "chat_name": None})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "chat_name is empty"

@patch('function.support_function.check_email_service')
@patch('service.ChatService.sf')
def test_query2_upgrade_old_no_answer(mock_function_chatbot, mock_user_repo):
    mock_user_repo.return_value = ("example@example.com",)
    list1 = []
    list2 = []
    mock_function_chatbot.handle_query_upgrade_keyword_old.return_value = None, list1, list2
    response = client.post("/chatbot/query/", data={"user_id": 1,
                                                    "text_all": json.dumps(text_all),
                                                    "question": "alo",
                                                    "chat_name": "test"})
    assert response.json()['status'] == 500
    assert response.json()['data']['message'] == "No answer"

@patch('function.support_function.check_email_service')
@patch('service.ChatService.sf')
@patch('service.ChatService.ChatHistoryRepository')
@patch('service.ChatService.DetailChatRepository')
def test_query2_upgrade_old_success(mock_detail_chat_repo, mock_chat_his_repo, mock_function_chatbot, mock_user_repo):
    mock_user_repo.return_value = ("example@example.com",)
    list1 = []
    list2 = []
    mock_function_chatbot.handle_query_upgrade_keyword_old.return_value = "success",list1,list2
    mock_chat_his_repo.getIdChatHistoryByUserIdAndNameChat.return_value = True
    mock_detail_chat_repo.addDetailChat.return_value = True
    response = client.post("/chatbot/query/", data={"user_id": 1,
                                                    "text_all": json.dumps(text_all),
                                                    "question": "123",
                                                    "chat_name": "test"})
    assert response.json()['status'] == 200
    assert response.json()['data']['answer'] == "success"

@patch('function.support_function.check_email_service')
@patch('service.ChatService.sf')
def test_extract_file_success(mock_function_chatbot, mock_user_repo):
    user_id = 1
    mock_user_repo.return_value = ("example@example.com",)
    mock_function_chatbot.extract_data2.return_value = "Success"
    response = client.get(f"/chatbot/extract_file/{user_id}")
    assert response.json()['status'] == 200
    assert response.json()['data']['text_all'] == "Success"



@patch('function.support_function.check_email_service')
def test_extract_file_id_not_exist(mock_user_repo):
    user_id = 1
    mock_user_repo.return_value = res.ReponseError(status=400, data=res.Message(
        message="Id not exist"))
    response = client.get(f"/chatbot/extract_file/{user_id}")
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Id not exist"

@patch('function.support_function.check_email_service')
def test_extract_file_email_empty(mock_user_repo):
    user_id = 1
    email = ""
    mock_user_repo.return_value = res.ReponseError(status=400, data=res.Message(
        message="Email is empty"))
    response = client.get(f"/chatbot/extract_file/{user_id}")
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Email is empty"

@patch('function.support_function.check_email_service')
def test_extract_file_email_in_valid(mock_user_repo):
    user_id = 1
    email = "202133123"
    mock_user_repo.return_value = res.ReponseError(status=400, data=res.Message(
        message="Email invalid"))
    response = client.get(f"/chatbot/extract_file/{user_id}")
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Email invalid"

@patch('function.support_function.check_email_service')
@patch('service.ChatService.sf')
def test_extract_file_no_data(mock_function_chatbot, mock_user_repo):
    user_id = 1
    email = "2021330@gmail.com"
    mock_user_repo.getEmailUserByIdFix.return_value = (email,)
    mock_function_chatbot.extract_data2.return_value = False
    response = client.get(f"/chatbot/extract_file/{user_id}")
    assert response.json()['status'] == 200
    assert response.json()['data']['text_all'] == "No data response"

@patch('function.support_function.check_email_service')
@patch('service.ChatService.sf')
def test_generate_question_success(mock_function_chatbot, mock_user_repo):
    user_id = 1
    mock_user_repo.return_value = ("example@example.com",)
    mock_function_chatbot.generate_question.return_value = ["Success"]
    response = client.get(f"/chatbot/generate_question/{user_id}")
    assert response.json()['status'] == 200
    assert response.json()['data']['question'] == ["Success"]

@patch('function.support_function.check_email_service')
def test_generate_question_id_not_exist(mock_user_repo):
    user_id = 1
    mock_user_repo.return_value = res.ReponseError(status=400, data=res.Message(
        message="Id not exist"))
    response = client.get(f"/chatbot/generate_question/{user_id}")
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Id not exist"

@patch('function.support_function.check_email_service')
def test_generate_question_email_empty(mock_user_repo):
    user_id = 1
    email = ""
    mock_user_repo.return_value = res.ReponseError(status=400, data=res.Message(
        message="Email is empty"))
    response = client.get(f"/chatbot/generate_question/{user_id}")
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Email is empty"


@patch('function.support_function.check_email_service')
def test_generate_question_email_in_valid(mock_user_repo):
    user_id = 1
    email = "202133123"
    mock_user_repo.return_value = res.ReponseError(status=400, data=res.Message(
        message="Email invalid"))
    response = client.get(f"/chatbot/generate_question/{user_id}")
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "Email invalid"

@patch('function.support_function.check_email_service')
@patch('service.ChatService.sf')
def test_generate_question_no_data(mock_function_chatbot, mock_user_repo):
    user_id = 1
    email = "2021330@gmail.com"
    mock_user_repo.return_value = (email,)
    mock_function_chatbot.generate_question.return_value = False
    response = client.get(f"/chatbot/generate_question/{user_id}")
    assert response.json()['status'] == 200
    assert response.json()['data']['question'] == False

def test_query_chatbot_user_id_required():
    user_id = None
    response = client.post("/chatbot/query/", data={"user_id": user_id,
                                                    "text_all": json.dumps(text_all),
                                                    "question": "12455",
                                                    "chat_name": "test"})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "user_id field is required."

def test_query_chatbot_user_id_interger():
    user_id = "aaaaa"
    response = client.post("/chatbot/query/", data={"user_id": user_id,
                                                    "text_all": json.dumps(text_all),
                                                    "question": "12455",
                                                    "chat_name": "test"})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "user_id must be an integer"

def test_query_chatbot_user_id_greater_0():
    user_id = "0"
    response = client.post("/chatbot/query/", data={"user_id": user_id,
                                                    "text_all": json.dumps(text_all),
                                                    "question": "12455",
                                                    "chat_name": "test"})
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "user_id must be greater than 0"




def test_extract_file_user_id_interger():
    user_id = "aaaaa"
    response = client.get(f"/chatbot/extract_file/{user_id}")
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "user_id must be an integer"

def test_extract_file_user_id_greater_0():
    user_id = "0"
    response = client.get(f"/chatbot/extract_file/{user_id}")
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "user_id must be greater than 0"

def test_generate_question_user_id_interger():
    user_id = "aaaaa"
    response = client.get(f"/chatbot/generate_question/{user_id}")
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "user_id must be an integer"

def test_generate_question_user_id_greater_0():
    user_id = "0"
    response = client.get(f"/chatbot/generate_question/{user_id}")
    assert response.json()['status'] == 400
    assert response.json()['data']['message'] == "user_id must be greater than 0"