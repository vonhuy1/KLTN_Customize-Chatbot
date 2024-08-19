import unittest
from unittest.mock import patch
import sys
import os
app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, app_path)
from service.ChatService import *
from request.RequestChat import *
from response.ResponseChat import *

class TestQuery2UpgradeOld(unittest.TestCase):
    @patch('service.ChatService.UserRepository')
    @patch('service.ChatService.sf')
    @patch('service.ChatService.support_function')
    def test_query2_upgrade_old_id_not_exist(self,mock_support_function, mock_function_chatbot, mock_user_repo):
        user_id = "1"
        text_all = 'aaa'
        question = 'chatbot la gi'
        chat_name = 'test'
        list1 = []
        list2 = []
        mock_function_chatbot.handle_query_upgrade_keyword_old.return_value = None, list1, list2
        mock_support_function.check_email_service.return_value = res.ReponseError(status=400, data=res.Message(
            message="Id not exist"))
        request = RequestQuery2UpgradeOld(user_id=user_id, text_all=text_all, question=question, chat_name=chat_name)
        response = query2_upgrade_old(request)
        self.assertIsInstance(response, ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data, Message(message='Id not exist'))
    
    @patch('service.ChatService.UserRepository')
    @patch('service.ChatService.sf')
    @patch('service.ChatService.support_function')
    def test_query2_upgrade_old_email_empty(self,mock_support_function, mock_function_chatbot, mock_user_repo):
        user_id = "1"
        email = None
        text_all = 'aaa'
        question = 'chatbot la gi'
        chat_name = 'test'
        mock_user_repo.getEmailUserByIdFix.return_value = (email,)
        list1 = []
        list2 = []
        mock_support_function.check_email_service.return_value = res.ReponseError(status=400, data=res.Message(
            message="Email is empty"))
        mock_function_chatbot.handle_query_upgrade_keyword_old.return_value = None, list1, list2

        request = RequestQuery2UpgradeOld(user_id=user_id, text_all=text_all, question=question, chat_name=chat_name)
        response = query2_upgrade_old(request)
        self.assertIsInstance(response, ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data, Message(message='Email is empty'))

    @patch('service.ChatService.UserRepository')
    @patch('service.ChatService.sf')
    @patch('service.ChatService.support_function')
    def test_query2_upgrade_old_email_in_valid(self,mock_support_function,mock_function_chatbot,mock_user_repo):
        user_id = "1"
        email = "20133118"
        text_all = 'aaa'
        question = 'chatbot la gi'
        chat_name = 'test'
        mock_user_repo.getEmailUserByIdFix.return_value = (email,)
        list1 = []
        list2 = []
        mock_support_function.check_email_service.return_value = res.ReponseError(status=400, data=res.Message(
            message="Email invalid"))
        mock_function_chatbot.handle_query_upgrade_keyword_old.return_value = None, list1, list2
        request = RequestQuery2UpgradeOld(user_id=user_id, text_all=text_all, question=question, chat_name=chat_name)
        response = query2_upgrade_old(request)
        self.assertIsInstance(response, ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data, Message(message='Email invalid'))

    @patch('service.ChatService.UserRepository')
    @patch('service.ChatService.sf')
    @patch('service.ChatService.support_function')
    def test_query2_upgrade_old_question_empty(self,mock_support_function,mock_function_chatbot, mock_user_repo):
        email = 'example@example.com'
        mock_user_repo.getEmailUserByIdFix.return_value = (email,)
        list1 = []
        list2 = []
        mock_support_function.check_email_service.return_value = email
        mock_function_chatbot.handle_query_upgrade_keyword_old.return_value = None, list1, list2
        request = RequestQuery2UpgradeOld(user_id="1", text_all="text aaa all", question=None, chat_name="test")
        response = query2_upgrade_old(request)
        self.assertIsInstance(response, ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data, Message(message='question is empty'))

    @patch('service.ChatService.UserRepository')
    @patch('service.ChatService.support_function')
    def test_query2_upgrade_old_chat_empty(self,mock_support_function, mock_user_repo):
        email = 'example@example.com'
        mock_support_function.check_email_service.return_value = email
        request = RequestQuery2UpgradeOld(user_id= "1", text_all="aaa bbb", question="aaa bbb", chat_name=None)
        response = query2_upgrade_old(request)
        self.assertIsInstance(response, ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data, Message(message='chat_name is empty'))

    @patch('service.ChatService.UserRepository')
    @patch('service.ChatService.sf')
    @patch('service.ChatService.support_function')
    def test_query2_upgrade_old_no_answer(self,mock_support_function, mock_function_chatbot, mock_user_repo):
        user_id = "1"
        email = 'example@example.com'
        text_all = [{"page_content":"Thành lập vào năm 2012, VMO Holdings (VMO) là công ty cung cấp dịch vụ CNTT chuyên nghiệp có trụ sở tại Việt Nam, Nhật Bản, Thái Lan và Mỹ. Với hơn 10 năm hoạt động trong lĩnh vực tư vấn và phát triển phần mềm, VMO hiện có hơn 1200 nhân sự và 9 văn phòng tại Việt Nam.\n\nHoàn thiện hệ sinh thái VMO và hướng tới giá trị cốt lõi trong tất cả các hoạt động, VMO tự tin trao quyền và niềm tin cho thế hệ kế cận. Chúng tôi luôn sẵn sàng chào đón các nhân tài cùng tham gia chinh phục thử thách trên những chặng đường sắp tới.\n\nTìm hiểu thêm về VMO Holdings qua:\n\n LinkedIn  Facebook  Website\n\nTHÔNG TIN TUYỂN DỤNG\n\nVị trí:\n\nĐịa điểm:\n\nBusiness Development Intern\n\nHà Nội\n\nKinh nghiệm:\n\nSố lượng:\n\nKhông yêu cầu kinh nghiệm 12\n\nMỨC HỖ TRỢ\n\nUpto 3M (Tùy theo năng lực) + Thưởng hoa hồng\n\nMÔ TẢ CÔNG VIỆC\n\nTham gia chương trình đào tạo miễn phí trong vòng 3 tháng theo lộ trình được\n\nxây dựng bài bản của công ty\n\nTham gia đào tạo các kỹ năng mềm, quy trình làm việc chuyên nghiệp  Trải nghiệm thực tế các công việc của một Business Developer như: + Tìm kiếm và kết nối với khách hàng + Giới thiệu sơ bộ về sản phẩm và dịch vụ công ty với khách hàng + Khai thác dữ liệu khách hàng\n\n[Type here]\n\nYÊU CẦU CÔNG VIỆC\n\nSử dụng Tiếng Anh thành thạo\n\nChăm chỉ, kiên nhẫn  Năng động, cởi mở, hòa đồng \n\nThông minh, tiếp thu nhanh, tư duy nhạy bén\n\nCó tinh thần cầu tiến trong công việc  Có kỹ năng giao tiếp và giải quyết vấn đề tốt  Có khả năng làm việc nhóm tốt  Đảm bảo làm việc full-time sau quá trình đào tạo\n\nQUYỀN LỢI\n\nCó cơ hội trở thành nhân viên chính thức tại VMO sau quá trình đào tạo   Được học tập với đội ngũ Mentors là Sales Manager, Teamlead có nhiều kinh nghiệm trong ngành Sales IT Global\n\nĐược tham gia các chương trình đào tạo nâng cao kỹ năng chuyên môn định kỳ\n\nhàng tháng\n\nĐược làm việc trực tiếp với khách hàng đa quốc gia thuộc nhiều lĩnh vực khác\n\nnhau\n\nĐược đào tạo trong môi trường năng động, trẻ trung, hiện đại và chuyên nghiệp\n\nCƠ HỘI VÀ THỬ THÁCH\n\nCơ hội được thử sức với các dự án hấp dẫn, thử thách đủ lớn trong và ngoài nước.  Cơ hội làm trải nghiệm môi trường làm việc cởi mở và năng động, khuyến khích trao đổi ý tưởng, trao quyền, cho phép làm việc, sáng tạo theo cách riêng. Tài năng và thành tích của từng nhân viên được trân trọng, nhân viên xuất sắc được khen thưởng hàng năm.\n\nCơ hội phát triển năng lực, được hỗ trợ phụ cấp chứng chỉ chuyên môn phục vụ công việc. Một số chứng chỉ cấp cao sẽ được chi trả toàn bộ chi phí từ học và thi.  Dự án khủng với domain hot-trend, liên tục cập nhật những công nghệ mới nhất Được làm việc trong môi trường có quy trình chuyên nghiệp, cùng những chuyên gia công nghệ đến từ các nước và khu vực khác nhau\n\n[Type here]\n\nVui lòng gửi CV của bạn về địa chỉ email: minhdn4@vmogroup.com\n\nEmail: minhdn4@vmogroup.com\n\nĐịa chỉ: Phòng Tuyển dụng – VMO Holdings, Tầng 20, Tòa IDMC, Số 18 Tôn Thất Thuyết, Mỹ Đình, Hà Nội.\n\n[Type here]","metadata":{"source":"/code/temp/vonhuytest123456789@gmail.com/JD_BD-Intern.pdf"},"type":"Document"}]
        question = "aaa bbb"
        chat_name = "test"
        mock_support_function.check_email_service.return_value = email
        list1 = []
        list2 = []
        mock_function_chatbot.handle_query_upgrade_keyword_old.return_value = None, list1, list2
        request = RequestQuery2UpgradeOld(user_id=user_id, text_all = json.dumps(text_all), question=question, chat_name=chat_name)
        response = query2_upgrade_old(request)
        self.assertIsInstance(response, ReponseError)
        self.assertEqual(response.status, 500)
        self.assertEqual(response.data.message, "No answer")
    
    @patch('service.ChatService.UserRepository')
    @patch('service.ChatService.sf')
    @patch('service.ChatService.ChatHistoryRepository')
    @patch('service.ChatService.DetailChatRepository')
    @patch('service.ChatService.support_function')
    def test_query2_upgrade_old_success(self,mock_support_function,mock_detail_chat_repo, mock_chat_his_repo, mock_function_chatbot, mock_user_repo):
        user_id = "1"
        email = 'example@example.com'
        text_all = [{"page_content":"Thành lập vào năm 2012, VMO Holdings (VMO) là công ty cung cấp dịch vụ CNTT chuyên nghiệp có trụ sở tại Việt Nam, Nhật Bản, Thái Lan và Mỹ. Với hơn 10 năm hoạt động trong lĩnh vực tư vấn và phát triển phần mềm, VMO hiện có hơn 1200 nhân sự và 9 văn phòng tại Việt Nam.\n\nHoàn thiện hệ sinh thái VMO và hướng tới giá trị cốt lõi trong tất cả các hoạt động, VMO tự tin trao quyền và niềm tin cho thế hệ kế cận. Chúng tôi luôn sẵn sàng chào đón các nhân tài cùng tham gia chinh phục thử thách trên những chặng đường sắp tới.\n\nTìm hiểu thêm về VMO Holdings qua:\n\n LinkedIn  Facebook  Website\n\nTHÔNG TIN TUYỂN DỤNG\n\nVị trí:\n\nĐịa điểm:\n\nBusiness Development Intern\n\nHà Nội\n\nKinh nghiệm:\n\nSố lượng:\n\nKhông yêu cầu kinh nghiệm 12\n\nMỨC HỖ TRỢ\n\nUpto 3M (Tùy theo năng lực) + Thưởng hoa hồng\n\nMÔ TẢ CÔNG VIỆC\n\nTham gia chương trình đào tạo miễn phí trong vòng 3 tháng theo lộ trình được\n\nxây dựng bài bản của công ty\n\nTham gia đào tạo các kỹ năng mềm, quy trình làm việc chuyên nghiệp  Trải nghiệm thực tế các công việc của một Business Developer như: + Tìm kiếm và kết nối với khách hàng + Giới thiệu sơ bộ về sản phẩm và dịch vụ công ty với khách hàng + Khai thác dữ liệu khách hàng\n\n[Type here]\n\nYÊU CẦU CÔNG VIỆC\n\nSử dụng Tiếng Anh thành thạo\n\nChăm chỉ, kiên nhẫn  Năng động, cởi mở, hòa đồng \n\nThông minh, tiếp thu nhanh, tư duy nhạy bén\n\nCó tinh thần cầu tiến trong công việc  Có kỹ năng giao tiếp và giải quyết vấn đề tốt  Có khả năng làm việc nhóm tốt  Đảm bảo làm việc full-time sau quá trình đào tạo\n\nQUYỀN LỢI\n\nCó cơ hội trở thành nhân viên chính thức tại VMO sau quá trình đào tạo   Được học tập với đội ngũ Mentors là Sales Manager, Teamlead có nhiều kinh nghiệm trong ngành Sales IT Global\n\nĐược tham gia các chương trình đào tạo nâng cao kỹ năng chuyên môn định kỳ\n\nhàng tháng\n\nĐược làm việc trực tiếp với khách hàng đa quốc gia thuộc nhiều lĩnh vực khác\n\nnhau\n\nĐược đào tạo trong môi trường năng động, trẻ trung, hiện đại và chuyên nghiệp\n\nCƠ HỘI VÀ THỬ THÁCH\n\nCơ hội được thử sức với các dự án hấp dẫn, thử thách đủ lớn trong và ngoài nước.  Cơ hội làm trải nghiệm môi trường làm việc cởi mở và năng động, khuyến khích trao đổi ý tưởng, trao quyền, cho phép làm việc, sáng tạo theo cách riêng. Tài năng và thành tích của từng nhân viên được trân trọng, nhân viên xuất sắc được khen thưởng hàng năm.\n\nCơ hội phát triển năng lực, được hỗ trợ phụ cấp chứng chỉ chuyên môn phục vụ công việc. Một số chứng chỉ cấp cao sẽ được chi trả toàn bộ chi phí từ học và thi.  Dự án khủng với domain hot-trend, liên tục cập nhật những công nghệ mới nhất Được làm việc trong môi trường có quy trình chuyên nghiệp, cùng những chuyên gia công nghệ đến từ các nước và khu vực khác nhau\n\n[Type here]\n\nVui lòng gửi CV của bạn về địa chỉ email: minhdn4@vmogroup.com\n\nEmail: minhdn4@vmogroup.com\n\nĐịa chỉ: Phòng Tuyển dụng – VMO Holdings, Tầng 20, Tòa IDMC, Số 18 Tôn Thất Thuyết, Mỹ Đình, Hà Nội.\n\n[Type here]","metadata":{"source":"/code/temp/vonhuytest123456789@gmail.com/JD_BD-Intern.pdf"},"type":"Document"}]
        question = "aaa bbb"
        chat_name = "test"
        mock_support_function.check_email_service.return_value = email
        list1 = []
        list2 = []
        mock_function_chatbot.handle_query_upgrade_keyword_old.return_value = "success",list1,list2
        mock_chat_his_repo.getIdChatHistoryByUserIdAndNameChat.return_value = True
        mock_detail_chat_repo.addDetailChat.return_value = True
        request = RequestQuery2UpgradeOld(user_id=user_id, text_all = json.dumps(text_all), question=question, chat_name=chat_name)
        response = query2_upgrade_old(request)
        self.assertIsInstance(response, ResponseQuery2UpgradeOld)
        self.assertEqual(response.status, 200)
        self.assertEqual(response.data.answer, "success")
    
    @patch('service.ChatService.UserRepository')
    @patch('service.ChatService.sf')
    @patch('service.ChatService.ChatHistoryRepository')
    @patch('service.ChatService.DetailChatRepository')
    @patch('service.ChatService.support_function')
    def test_query2_upgrade_old_server_error_user_repo(self,mock_support_function,mock_detail_chat_repo, mock_chat_his_repo, mock_function_chatbot, mock_user_repo):
        user_id = "1"
        email = 'example@example.com'
        text_all = [{"page_content":"Thành lập vào năm 2012, VMO Holdings (VMO) là công ty cung cấp dịch vụ CNTT chuyên nghiệp có trụ sở tại Việt Nam, Nhật Bản, Thái Lan và Mỹ. Với hơn 10 năm hoạt động trong lĩnh vực tư vấn và phát triển phần mềm, VMO hiện có hơn 1200 nhân sự và 9 văn phòng tại Việt Nam.\n\nHoàn thiện hệ sinh thái VMO và hướng tới giá trị cốt lõi trong tất cả các hoạt động, VMO tự tin trao quyền và niềm tin cho thế hệ kế cận. Chúng tôi luôn sẵn sàng chào đón các nhân tài cùng tham gia chinh phục thử thách trên những chặng đường sắp tới.\n\nTìm hiểu thêm về VMO Holdings qua:\n\n LinkedIn  Facebook  Website\n\nTHÔNG TIN TUYỂN DỤNG\n\nVị trí:\n\nĐịa điểm:\n\nBusiness Development Intern\n\nHà Nội\n\nKinh nghiệm:\n\nSố lượng:\n\nKhông yêu cầu kinh nghiệm 12\n\nMỨC HỖ TRỢ\n\nUpto 3M (Tùy theo năng lực) + Thưởng hoa hồng\n\nMÔ TẢ CÔNG VIỆC\n\nTham gia chương trình đào tạo miễn phí trong vòng 3 tháng theo lộ trình được\n\nxây dựng bài bản của công ty\n\nTham gia đào tạo các kỹ năng mềm, quy trình làm việc chuyên nghiệp  Trải nghiệm thực tế các công việc của một Business Developer như: + Tìm kiếm và kết nối với khách hàng + Giới thiệu sơ bộ về sản phẩm và dịch vụ công ty với khách hàng + Khai thác dữ liệu khách hàng\n\n[Type here]\n\nYÊU CẦU CÔNG VIỆC\n\nSử dụng Tiếng Anh thành thạo\n\nChăm chỉ, kiên nhẫn  Năng động, cởi mở, hòa đồng \n\nThông minh, tiếp thu nhanh, tư duy nhạy bén\n\nCó tinh thần cầu tiến trong công việc  Có kỹ năng giao tiếp và giải quyết vấn đề tốt  Có khả năng làm việc nhóm tốt  Đảm bảo làm việc full-time sau quá trình đào tạo\n\nQUYỀN LỢI\n\nCó cơ hội trở thành nhân viên chính thức tại VMO sau quá trình đào tạo   Được học tập với đội ngũ Mentors là Sales Manager, Teamlead có nhiều kinh nghiệm trong ngành Sales IT Global\n\nĐược tham gia các chương trình đào tạo nâng cao kỹ năng chuyên môn định kỳ\n\nhàng tháng\n\nĐược làm việc trực tiếp với khách hàng đa quốc gia thuộc nhiều lĩnh vực khác\n\nnhau\n\nĐược đào tạo trong môi trường năng động, trẻ trung, hiện đại và chuyên nghiệp\n\nCƠ HỘI VÀ THỬ THÁCH\n\nCơ hội được thử sức với các dự án hấp dẫn, thử thách đủ lớn trong và ngoài nước.  Cơ hội làm trải nghiệm môi trường làm việc cởi mở và năng động, khuyến khích trao đổi ý tưởng, trao quyền, cho phép làm việc, sáng tạo theo cách riêng. Tài năng và thành tích của từng nhân viên được trân trọng, nhân viên xuất sắc được khen thưởng hàng năm.\n\nCơ hội phát triển năng lực, được hỗ trợ phụ cấp chứng chỉ chuyên môn phục vụ công việc. Một số chứng chỉ cấp cao sẽ được chi trả toàn bộ chi phí từ học và thi.  Dự án khủng với domain hot-trend, liên tục cập nhật những công nghệ mới nhất Được làm việc trong môi trường có quy trình chuyên nghiệp, cùng những chuyên gia công nghệ đến từ các nước và khu vực khác nhau\n\n[Type here]\n\nVui lòng gửi CV của bạn về địa chỉ email: minhdn4@vmogroup.com\n\nEmail: minhdn4@vmogroup.com\n\nĐịa chỉ: Phòng Tuyển dụng – VMO Holdings, Tầng 20, Tòa IDMC, Số 18 Tôn Thất Thuyết, Mỹ Đình, Hà Nội.\n\n[Type here]","metadata":{"source":"/code/temp/vonhuytest123456789@gmail.com/JD_BD-Intern.pdf"},"type":"Document"}]
        question = "aaa bbb"
        chat_name = "test"
        mock_support_function.check_email_service.side_effect = Exception("Unexpected Error")
        list1 = []
        list2 = []
        mock_function_chatbot.handle_query_upgrade_keyword_old.return_value = None, list1, list2
        request = RequestQuery2UpgradeOld(user_id=user_id, text_all = json.dumps(text_all), question=question, chat_name=chat_name)
        response = query2_upgrade_old(request)
        self.assertIsInstance(response, ReponseError)
        self.assertEqual(response.status, 500)
        self.assertEqual(response.data.message, "Server Error")
    
    @patch('service.ChatService.UserRepository')
    @patch('service.ChatService.sf')
    @patch('service.ChatService.ChatHistoryRepository')
    @patch('service.ChatService.DetailChatRepository')
    @patch('service.ChatService.support_function')
    def test_query2_upgrade_old_server_error_chathistory_repo(self,mock_support_function,mock_detail_chat_repo, mock_chat_his_repo, mock_function_chatbot, mock_user_repo):
        user_id = "1"
        email = 'example@example.com'
        text_all = [{"page_content":"Thành lập vào năm 2012, VMO Holdings (VMO) là công ty cung cấp dịch vụ CNTT chuyên nghiệp có trụ sở tại Việt Nam, Nhật Bản, Thái Lan và Mỹ. Với hơn 10 năm hoạt động trong lĩnh vực tư vấn và phát triển phần mềm, VMO hiện có hơn 1200 nhân sự và 9 văn phòng tại Việt Nam.\n\nHoàn thiện hệ sinh thái VMO và hướng tới giá trị cốt lõi trong tất cả các hoạt động, VMO tự tin trao quyền và niềm tin cho thế hệ kế cận. Chúng tôi luôn sẵn sàng chào đón các nhân tài cùng tham gia chinh phục thử thách trên những chặng đường sắp tới.\n\nTìm hiểu thêm về VMO Holdings qua:\n\n LinkedIn  Facebook  Website\n\nTHÔNG TIN TUYỂN DỤNG\n\nVị trí:\n\nĐịa điểm:\n\nBusiness Development Intern\n\nHà Nội\n\nKinh nghiệm:\n\nSố lượng:\n\nKhông yêu cầu kinh nghiệm 12\n\nMỨC HỖ TRỢ\n\nUpto 3M (Tùy theo năng lực) + Thưởng hoa hồng\n\nMÔ TẢ CÔNG VIỆC\n\nTham gia chương trình đào tạo miễn phí trong vòng 3 tháng theo lộ trình được\n\nxây dựng bài bản của công ty\n\nTham gia đào tạo các kỹ năng mềm, quy trình làm việc chuyên nghiệp  Trải nghiệm thực tế các công việc của một Business Developer như: + Tìm kiếm và kết nối với khách hàng + Giới thiệu sơ bộ về sản phẩm và dịch vụ công ty với khách hàng + Khai thác dữ liệu khách hàng\n\n[Type here]\n\nYÊU CẦU CÔNG VIỆC\n\nSử dụng Tiếng Anh thành thạo\n\nChăm chỉ, kiên nhẫn  Năng động, cởi mở, hòa đồng \n\nThông minh, tiếp thu nhanh, tư duy nhạy bén\n\nCó tinh thần cầu tiến trong công việc  Có kỹ năng giao tiếp và giải quyết vấn đề tốt  Có khả năng làm việc nhóm tốt  Đảm bảo làm việc full-time sau quá trình đào tạo\n\nQUYỀN LỢI\n\nCó cơ hội trở thành nhân viên chính thức tại VMO sau quá trình đào tạo   Được học tập với đội ngũ Mentors là Sales Manager, Teamlead có nhiều kinh nghiệm trong ngành Sales IT Global\n\nĐược tham gia các chương trình đào tạo nâng cao kỹ năng chuyên môn định kỳ\n\nhàng tháng\n\nĐược làm việc trực tiếp với khách hàng đa quốc gia thuộc nhiều lĩnh vực khác\n\nnhau\n\nĐược đào tạo trong môi trường năng động, trẻ trung, hiện đại và chuyên nghiệp\n\nCƠ HỘI VÀ THỬ THÁCH\n\nCơ hội được thử sức với các dự án hấp dẫn, thử thách đủ lớn trong và ngoài nước.  Cơ hội làm trải nghiệm môi trường làm việc cởi mở và năng động, khuyến khích trao đổi ý tưởng, trao quyền, cho phép làm việc, sáng tạo theo cách riêng. Tài năng và thành tích của từng nhân viên được trân trọng, nhân viên xuất sắc được khen thưởng hàng năm.\n\nCơ hội phát triển năng lực, được hỗ trợ phụ cấp chứng chỉ chuyên môn phục vụ công việc. Một số chứng chỉ cấp cao sẽ được chi trả toàn bộ chi phí từ học và thi.  Dự án khủng với domain hot-trend, liên tục cập nhật những công nghệ mới nhất Được làm việc trong môi trường có quy trình chuyên nghiệp, cùng những chuyên gia công nghệ đến từ các nước và khu vực khác nhau\n\n[Type here]\n\nVui lòng gửi CV của bạn về địa chỉ email: minhdn4@vmogroup.com\n\nEmail: minhdn4@vmogroup.com\n\nĐịa chỉ: Phòng Tuyển dụng – VMO Holdings, Tầng 20, Tòa IDMC, Số 18 Tôn Thất Thuyết, Mỹ Đình, Hà Nội.\n\n[Type here]","metadata":{"source":"/code/temp/vonhuytest123456789@gmail.com/JD_BD-Intern.pdf"},"type":"Document"}]
        question = "aaa bbb"
        chat_name = "test"
        mock_chat_his_repo.side_effect = Exception("Unexpected Error")
        request = RequestQuery2UpgradeOld(user_id=user_id, text_all = json.dumps(text_all), question=question, chat_name=chat_name)
        response = query2_upgrade_old(request)
        self.assertIsInstance(response, ReponseError)
        self.assertEqual(response.status, 500)
        self.assertEqual(response.data.message, "Server Error")
    
    @patch('service.ChatService.UserRepository')
    @patch('service.ChatService.sf')
    @patch('service.ChatService.ChatHistoryRepository')
    @patch('service.ChatService.DetailChatRepository')
    @patch('service.ChatService.support_function')
    def test_query2_upgrade_old_server_error_detailchat_repo(self,mock_support_function,mock_detail_chat_repo, mock_chat_his_repo, mock_function_chatbot, mock_user_repo):
        user_id = "1"
        email = 'example@example.com'
        text_all = [{"page_content":"Thành lập vào năm 2012, VMO Holdings (VMO) là công ty cung cấp dịch vụ CNTT chuyên nghiệp có trụ sở tại Việt Nam, Nhật Bản, Thái Lan và Mỹ. Với hơn 10 năm hoạt động trong lĩnh vực tư vấn và phát triển phần mềm, VMO hiện có hơn 1200 nhân sự và 9 văn phòng tại Việt Nam.\n\nHoàn thiện hệ sinh thái VMO và hướng tới giá trị cốt lõi trong tất cả các hoạt động, VMO tự tin trao quyền và niềm tin cho thế hệ kế cận. Chúng tôi luôn sẵn sàng chào đón các nhân tài cùng tham gia chinh phục thử thách trên những chặng đường sắp tới.\n\nTìm hiểu thêm về VMO Holdings qua:\n\n LinkedIn  Facebook  Website\n\nTHÔNG TIN TUYỂN DỤNG\n\nVị trí:\n\nĐịa điểm:\n\nBusiness Development Intern\n\nHà Nội\n\nKinh nghiệm:\n\nSố lượng:\n\nKhông yêu cầu kinh nghiệm 12\n\nMỨC HỖ TRỢ\n\nUpto 3M (Tùy theo năng lực) + Thưởng hoa hồng\n\nMÔ TẢ CÔNG VIỆC\n\nTham gia chương trình đào tạo miễn phí trong vòng 3 tháng theo lộ trình được\n\nxây dựng bài bản của công ty\n\nTham gia đào tạo các kỹ năng mềm, quy trình làm việc chuyên nghiệp  Trải nghiệm thực tế các công việc của một Business Developer như: + Tìm kiếm và kết nối với khách hàng + Giới thiệu sơ bộ về sản phẩm và dịch vụ công ty với khách hàng + Khai thác dữ liệu khách hàng\n\n[Type here]\n\nYÊU CẦU CÔNG VIỆC\n\nSử dụng Tiếng Anh thành thạo\n\nChăm chỉ, kiên nhẫn  Năng động, cởi mở, hòa đồng \n\nThông minh, tiếp thu nhanh, tư duy nhạy bén\n\nCó tinh thần cầu tiến trong công việc  Có kỹ năng giao tiếp và giải quyết vấn đề tốt  Có khả năng làm việc nhóm tốt  Đảm bảo làm việc full-time sau quá trình đào tạo\n\nQUYỀN LỢI\n\nCó cơ hội trở thành nhân viên chính thức tại VMO sau quá trình đào tạo   Được học tập với đội ngũ Mentors là Sales Manager, Teamlead có nhiều kinh nghiệm trong ngành Sales IT Global\n\nĐược tham gia các chương trình đào tạo nâng cao kỹ năng chuyên môn định kỳ\n\nhàng tháng\n\nĐược làm việc trực tiếp với khách hàng đa quốc gia thuộc nhiều lĩnh vực khác\n\nnhau\n\nĐược đào tạo trong môi trường năng động, trẻ trung, hiện đại và chuyên nghiệp\n\nCƠ HỘI VÀ THỬ THÁCH\n\nCơ hội được thử sức với các dự án hấp dẫn, thử thách đủ lớn trong và ngoài nước.  Cơ hội làm trải nghiệm môi trường làm việc cởi mở và năng động, khuyến khích trao đổi ý tưởng, trao quyền, cho phép làm việc, sáng tạo theo cách riêng. Tài năng và thành tích của từng nhân viên được trân trọng, nhân viên xuất sắc được khen thưởng hàng năm.\n\nCơ hội phát triển năng lực, được hỗ trợ phụ cấp chứng chỉ chuyên môn phục vụ công việc. Một số chứng chỉ cấp cao sẽ được chi trả toàn bộ chi phí từ học và thi.  Dự án khủng với domain hot-trend, liên tục cập nhật những công nghệ mới nhất Được làm việc trong môi trường có quy trình chuyên nghiệp, cùng những chuyên gia công nghệ đến từ các nước và khu vực khác nhau\n\n[Type here]\n\nVui lòng gửi CV của bạn về địa chỉ email: minhdn4@vmogroup.com\n\nEmail: minhdn4@vmogroup.com\n\nĐịa chỉ: Phòng Tuyển dụng – VMO Holdings, Tầng 20, Tòa IDMC, Số 18 Tôn Thất Thuyết, Mỹ Đình, Hà Nội.\n\n[Type here]","metadata":{"source":"/code/temp/vonhuytest123456789@gmail.com/JD_BD-Intern.pdf"},"type":"Document"}]
        question = "aaa bbb"
        chat_name = "test"
        mock_support_function.check_email_service.return_value = email
        mock_detail_chat_repo.side_effect = Exception("Unexpected Error")
        request = RequestQuery2UpgradeOld(user_id=user_id, text_all = json.dumps(text_all), question=question, chat_name=chat_name)
        response = query2_upgrade_old(request)
        self.assertIsInstance(response, ReponseError)
        self.assertEqual(response.status, 500)
        self.assertEqual(response.data.message, "Server Error")
    
    @patch('service.ChatService.UserRepository')
    @patch('service.ChatService.sf')
    @patch('service.ChatService.ChatHistoryRepository')
    @patch('service.ChatService.DetailChatRepository')
    @patch('service.ChatService.support_function')
    def test_query2_upgrade_old_server_error_function_repo(self,mock_support_function,mock_detail_chat_repo, mock_chat_his_repo, mock_function_chatbot, mock_user_repo):
        user_id = "1"
        email = 'example@example.com'
        text_all = [{"page_content":"Thành lập vào năm 2012, VMO Holdings (VMO) là công ty cung cấp dịch vụ CNTT chuyên nghiệp có trụ sở tại Việt Nam, Nhật Bản, Thái Lan và Mỹ. Với hơn 10 năm hoạt động trong lĩnh vực tư vấn và phát triển phần mềm, VMO hiện có hơn 1200 nhân sự và 9 văn phòng tại Việt Nam.\n\nHoàn thiện hệ sinh thái VMO và hướng tới giá trị cốt lõi trong tất cả các hoạt động, VMO tự tin trao quyền và niềm tin cho thế hệ kế cận. Chúng tôi luôn sẵn sàng chào đón các nhân tài cùng tham gia chinh phục thử thách trên những chặng đường sắp tới.\n\nTìm hiểu thêm về VMO Holdings qua:\n\n LinkedIn  Facebook  Website\n\nTHÔNG TIN TUYỂN DỤNG\n\nVị trí:\n\nĐịa điểm:\n\nBusiness Development Intern\n\nHà Nội\n\nKinh nghiệm:\n\nSố lượng:\n\nKhông yêu cầu kinh nghiệm 12\n\nMỨC HỖ TRỢ\n\nUpto 3M (Tùy theo năng lực) + Thưởng hoa hồng\n\nMÔ TẢ CÔNG VIỆC\n\nTham gia chương trình đào tạo miễn phí trong vòng 3 tháng theo lộ trình được\n\nxây dựng bài bản của công ty\n\nTham gia đào tạo các kỹ năng mềm, quy trình làm việc chuyên nghiệp  Trải nghiệm thực tế các công việc của một Business Developer như: + Tìm kiếm và kết nối với khách hàng + Giới thiệu sơ bộ về sản phẩm và dịch vụ công ty với khách hàng + Khai thác dữ liệu khách hàng\n\n[Type here]\n\nYÊU CẦU CÔNG VIỆC\n\nSử dụng Tiếng Anh thành thạo\n\nChăm chỉ, kiên nhẫn  Năng động, cởi mở, hòa đồng \n\nThông minh, tiếp thu nhanh, tư duy nhạy bén\n\nCó tinh thần cầu tiến trong công việc  Có kỹ năng giao tiếp và giải quyết vấn đề tốt  Có khả năng làm việc nhóm tốt  Đảm bảo làm việc full-time sau quá trình đào tạo\n\nQUYỀN LỢI\n\nCó cơ hội trở thành nhân viên chính thức tại VMO sau quá trình đào tạo   Được học tập với đội ngũ Mentors là Sales Manager, Teamlead có nhiều kinh nghiệm trong ngành Sales IT Global\n\nĐược tham gia các chương trình đào tạo nâng cao kỹ năng chuyên môn định kỳ\n\nhàng tháng\n\nĐược làm việc trực tiếp với khách hàng đa quốc gia thuộc nhiều lĩnh vực khác\n\nnhau\n\nĐược đào tạo trong môi trường năng động, trẻ trung, hiện đại và chuyên nghiệp\n\nCƠ HỘI VÀ THỬ THÁCH\n\nCơ hội được thử sức với các dự án hấp dẫn, thử thách đủ lớn trong và ngoài nước.  Cơ hội làm trải nghiệm môi trường làm việc cởi mở và năng động, khuyến khích trao đổi ý tưởng, trao quyền, cho phép làm việc, sáng tạo theo cách riêng. Tài năng và thành tích của từng nhân viên được trân trọng, nhân viên xuất sắc được khen thưởng hàng năm.\n\nCơ hội phát triển năng lực, được hỗ trợ phụ cấp chứng chỉ chuyên môn phục vụ công việc. Một số chứng chỉ cấp cao sẽ được chi trả toàn bộ chi phí từ học và thi.  Dự án khủng với domain hot-trend, liên tục cập nhật những công nghệ mới nhất Được làm việc trong môi trường có quy trình chuyên nghiệp, cùng những chuyên gia công nghệ đến từ các nước và khu vực khác nhau\n\n[Type here]\n\nVui lòng gửi CV của bạn về địa chỉ email: minhdn4@vmogroup.com\n\nEmail: minhdn4@vmogroup.com\n\nĐịa chỉ: Phòng Tuyển dụng – VMO Holdings, Tầng 20, Tòa IDMC, Số 18 Tôn Thất Thuyết, Mỹ Đình, Hà Nội.\n\n[Type here]","metadata":{"source":"/code/temp/vonhuytest123456789@gmail.com/JD_BD-Intern.pdf"},"type":"Document"}]
        question = "aaa bbb"
        chat_name = "test"
        mock_support_function.check_email_service.return_value = email
        mock_function_chatbot.side_effect = Exception("Unexpected Error")
        request = RequestQuery2UpgradeOld(user_id=user_id, text_all = json.dumps(text_all), question=question, chat_name=chat_name)
        response = query2_upgrade_old(request)
        self.assertIsInstance(response, ReponseError)
        self.assertEqual(response.status, 500)
        self.assertEqual(response.data.message, "Server Error")
    
class TestExtractFile(unittest.TestCase):
    @patch('service.ChatService.UserRepository')
    @patch('service.ChatService.sf')
    @patch('service.ChatService.support_function')
    def test_extract_file_success(self,mock_support_function, mock_function_chatbot, mock_user_repo):
        user_id = "1"
        email = 'example@example.com'
        mock_support_function.check_email_service.return_value = email
        mock_function_chatbot.extract_data2.return_value = True
        request = RequestExtractFile(user_id=user_id)
        response = extract_file(request)
        self.assertIsInstance(response, ResponseExtractFile)
        self.assertEqual(response.status, 200)

    @patch('service.ChatService.UserRepository')
    @patch('service.ChatService.sf')
    @patch('service.ChatService.support_function')
    def test_extract_file_id_not_exist(self,mock_support_function, mock_function_chatbot, mock_user_repo):
        user_id = "1"
        mock_support_function.check_email_service.return_value = res.ReponseError(status=400, data=res.Message(
            message="Id not exist"))
        request = RequestExtractFile(user_id=user_id)
        response = extract_file(request)
        self.assertIsInstance(response, ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data, Message(message='Id not exist'))
    
    @patch('service.ChatService.UserRepository')
    @patch('service.ChatService.sf')
    @patch('service.ChatService.support_function')
    def test_extract_file_email_empty(self,mock_support_function,mock_function_chatbot, mock_user_repo):
        user_id = "1"
        email = None
        mock_support_function.check_email_service.return_value = res.ReponseError(status=400, data=res.Message(
            message="Email is empty"))
        request = RequestExtractFile(user_id=user_id)
        response = extract_file(request)
        self.assertIsInstance(response, ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data, Message(message='Email is empty'))

    @patch('service.ChatService.UserRepository')
    @patch('service.ChatService.sf')
    @patch('service.ChatService.support_function')
    def test_extract_file_email_in_valid(self,mock_support_function
, mock_function_chatbot, mock_user_repo):
        user_id = "1"
        mock_support_function.check_email_service.return_value = res.ReponseError(status=400, data=res.Message(
            message="Email invalid"))
        request = RequestExtractFile(user_id=user_id)
        response = extract_file(request)
        self.assertIsInstance(response, ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data, Message(message='Email invalid'))
    
    @patch('service.ChatService.UserRepository')
    @patch('service.ChatService.sf')
    @patch('service.ChatService.support_function')
    def test_extract_file_no_data(self, mock_support_function, mock_function_chatbot, mock_user_repo):
        user_id = "1"
        email = 'example@example.com'
        mock_support_function.check_email_service.return_value = email
        mock_function_chatbot.extract_data2.return_value = False
        request = RequestExtractFile(user_id=user_id)
        response = extract_file(request)
        self.assertIsInstance(response, ResponseExtractFile)
        self.assertEqual(response.status, 200)
        self.assertEqual(response.data, DataExtractFile(text_all="No data response"))
    
    @patch('service.ChatService.UserRepository')
    @patch('service.ChatService.sf')
    @patch('service.ChatService.support_function')
    def test_extract_file_server_error_sf(self, mock_support_function,mock_function_chatbot, mock_user_repo):
        user_id = "1"
        email = None
        mock_support_function.check_email_service.side_effect = Exception("Unexpected Error")
        request = RequestExtractFile(user_id=user_id)
        response = extract_file(request)
        self.assertIsInstance(response, ReponseError)
        self.assertEqual(response.status, 500)
        self.assertEqual(response.data, Message(message='Server Error'))

class TestGenerateQuestion(unittest.TestCase):
    @patch('service.ChatService.UserRepository')
    @patch('service.ChatService.sf')
    @patch('service.ChatService.support_function')
    def test_generate_question_success(self,mock_support_function, mock_function_chatbot, mock_user_repo):
        user_id = "1"
        email = 'example@example.com'
        mock_support_function.check_email_service.return_value = email
        mock_function_chatbot.generate_question.return_value = True
        request = RequestGenerateQuestion(user_id=user_id)
        response = generate_question(request)
        self.assertIsInstance(response, ResponseGenerateQuestion)
        self.assertEqual(response.status, 200)

    @patch('service.ChatService.UserRepository')
    @patch('service.ChatService.sf')
    @patch('service.ChatService.support_function')
    def test_generate_question_id_not_exist(self,mock_support_function, mock_function_chatbot, mock_user_repo):
        user_id = "1"
        mock_support_function.check_email_service.return_value = res.ReponseError(status=400, data=res.Message(
            message="Id not exist"))
        request = RequestGenerateQuestion(user_id=user_id)
        response = generate_question(request)
        self.assertIsInstance(response, ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data, Message(message='Id not exist'))
    
    @patch('service.ChatService.UserRepository')
    @patch('service.ChatService.sf')
    @patch('service.ChatService.support_function')
    def test_generate_question_email_empty(self,mock_support_function, mock_function_chatbot, mock_user_repo):
        user_id = "1"
        mock_support_function.check_email_service.return_value = res.ReponseError(status=400, data=res.Message(
            message="Email is empty"))
        request = RequestGenerateQuestion(user_id=user_id)
        response = generate_question(request)
        self.assertIsInstance(response, ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data, Message(message='Email is empty'))

    @patch('service.ChatService.UserRepository')
    @patch('service.ChatService.sf')
    @patch('service.ChatService.support_function')
    def test_generate_question_email_in_valid(self,mock_support_function, mock_function_chatbot, mock_user_repo):
        user_id = "1"
        email = "20133118"
        mock_support_function.check_email_service.return_value = res.ReponseError(status=400, data=res.Message(
            message="Email invalid"))
        request = RequestGenerateQuestion(user_id=user_id)
        response = generate_question(request)
        self.assertIsInstance(response, ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data, Message(message='Email invalid'))
    
    @patch('service.ChatService.UserRepository')
    @patch('service.ChatService.sf')
    @patch('service.ChatService.support_function')
    def test_generate_question_no_data(self,mock_support_function, mock_function_chatbot, mock_user_repo):
        user_id = "1"
        email = 'example@example.com'
        mock_support_function.check_email_service.return_value = email
        mock_function_chatbot.generate_question.return_value = False
        request = RequestGenerateQuestion(user_id=user_id)
        response = generate_question(request)
        self.assertIsInstance(response, ResponseGenerateQuestion)
        self.assertEqual(response.status, 200)
        self.assertEqual(response.data, GenerateQuestion(question=False))
    
    @patch('service.ChatService.UserRepository')
    @patch('service.ChatService.sf')
    @patch('service.ChatService.support_function')
    def test_generate_question_server_err_user_repo(self,mock_support_function
, mock_function_chatbot, mock_user_repo):
        user_id = "1"
        email = None
        mock_support_function.side_effect = Exception("Unexpected Error")
        request = RequestGenerateQuestion(user_id=user_id)
        response = generate_question(request)
        self.assertIsInstance(response, ReponseError)
        self.assertEqual(response.status, 500)
        self.assertEqual(response.data, Message(message='Server Error'))

class TestDeleteChat(unittest.TestCase):
    @patch('service.ChatService.UserRepository')
    @patch('service.ChatService.DetailChatRepository')
    @patch('service.ChatService.ChatHistoryRepository')
    @patch('service.ChatService.support_function')
    def test_delete_chat_success(self, mock_support_function, mock_detail_chat_repo, mock_chat_history_repo, mock_user_repo):
        user_id = "1"
        email = 'example@example.com'
        chat_name = 'test'
        mock_support_function.check_email_service.return_value = email
        mock_detail_chat_repo.delete_chat_detail.return_value = True
        mock_chat_history_repo.deleteChatHistory.return_value = True
        request = RequestDeleteChat(user_id=user_id, chat_name=chat_name)
        response = delete_chat(request)
        self.assertIsInstance(response, ResponseDeleteChat)
        self.assertEqual(response.status, 200)
        self.assertEqual(response.data, Message(message="Delete conversation chat success"))

    @patch('service.ChatService.UserRepository')
    @patch('service.ChatService.support_function')
    def test_delete_chat_id_not_exist(self,mock_support_function, mock_user_repo):
        user_id = "1"
        chat_name = 'test'
        mock_support_function.check_email_service.return_value = res.ReponseError(status=400, data=res.Message(
            message="Id not exist"))
        request = RequestDeleteChat(user_id=user_id, chat_name=chat_name)
        response = delete_chat(request)
        self.assertIsInstance(response, ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data, Message(message='Id not exist'))
    
    @patch('service.ChatService.UserRepository')
    @patch('service.ChatService.support_function')
    def test_delete_chat_chat_name_empty(self, mock_support_function, mock_user_repo):
        user_id = "1"
        email = 'example@example.com'
        chat_name = None
        mock_support_function.check_email_service.return_value = email
        request = RequestDeleteChat(user_id=user_id, chat_name=chat_name)
        response = delete_chat(request)
        self.assertIsInstance(response, ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message, "chat_name is empty")
    
    @patch('service.ChatService.UserRepository')
    @patch('service.ChatService.ChatHistoryRepository')
    @patch('service.ChatService.support_function')
    def test_delete_chat_failed(self,mock_support_function, mock_chat_history_repo, mock_user_repo):
        user_id = "1"
        email = 'example@example.com'
        chat_name = 'test'
        mock_support_function.check_email_service.return_value = email
        mock_chat_history_repo.deleteChatHistory.return_value = False
        request = RequestDeleteChat(user_id=user_id, chat_name=chat_name)
        response = delete_chat(request)
        self.assertIsInstance(response, ResponseDeleteChat)
        self.assertEqual(response.status, 500)
        self.assertEqual(response.data, Message(message="Delete conversation chat failed"))

    @patch('service.ChatService.support_function')
    @patch('service.ChatService.DetailChatRepository.delete_chat_detail')
    @patch('service.ChatService.ChatHistoryRepository.deleteChatHistory')
    def test_delete_chat_server_err(self, mock_chat_history_repo, mock_detail_chat_repo, mock_support_function):
        user_id = "1"
        chat_name = 'test'

        mock_support_function.check_email_service.side_effect = Exception("Unexpected Error")

        request = RequestDeleteChat(user_id=user_id, chat_name=chat_name)
        response = delete_chat(request)

        # Assuming ReponseError is the correct class name
        self.assertIsInstance(response, res.ReponseError)  # Check against ReponseError
        self.assertEqual(response.status, 500)
        self.assertEqual(response.data.message, "Server Error")


if __name__ == '__main__':
    unittest.main()