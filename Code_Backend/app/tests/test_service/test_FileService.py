import unittest
from unittest.mock import patch,MagicMock
import sys
import os
app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, app_path)
from fastapi import UploadFile
from io import BytesIO
import tempfile
from service.FileService import deleteFile,download_folder,download_file,upload_files,deleteAllFile,listNameFiles
from request.RequestFile import RequestDeleteAllFile,RequestDeleteFile,RequestDownLoadFile,RequestDownLoadFolder,RequestGetNameFile,RequestUploadFile
from response import ResponseFile as res
from response import ResponseDefault as res1

class TestDeleteFile(unittest.TestCase):
    @patch('service.FileService.UserRepository')
    @patch('service.FileService.sf.check_email_service',return_value = 'example@example.com')
    def test_delete_file_success(self,mock_support_function,mock_user_repo):
        user_id = "1"
        email = 'example@example.com'
        name_file = "test1.pdf"
        request = RequestDeleteFile(user_id=user_id,name_file=name_file)
        response = deleteFile(request)
        self.assertIsInstance(response, res.ResponseDeleteFile)
        self.assertEqual(response.status, 200)
    
    @patch('service.FileService.UserRepository')
    @patch('service.FileService.sf.check_email_service', return_value=res1.ReponseError(status=400,data=res.Message(
            message="Id not exist")))
    def test_delete_file_id_not_exist(self, mock_support_function,  mock_user_repo):
        user_id = "1"
        email = 'example@example.com'
        name_file = "test1.pdf"

        request = RequestDeleteFile(user_id=user_id,name_file=name_file)
        response = deleteFile(request)
        self.assertIsInstance(response, res1.ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data, res.Message(message='Id not exist'))
    
    @patch('service.FileService.UserRepository')
    @patch('service.FileService.sf.check_email_service', return_value=res1.ReponseError(status=400, data=res.Message(
        message="Email is empty")))
    def test_delete_file_email_empty(self,mock_support_function, mock_user_repo):
        user_id = "1"
        email = None
        name_file = "test1.pdf"
        mock_user_repo.getEmailUserByIdFix.return_value = (email,)
        request = RequestDeleteFile(user_id=user_id,name_file=name_file)
        response = deleteFile(request)
        self.assertIsInstance(response, res1.ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data, res.Message(message='Email is empty'))
    
    @patch('service.FileService.UserRepository')
    @patch('service.FileService.sf.check_email_service', return_value=res1.ReponseError(status=400, data=res.Message(
        message="Email invalid")))
    def test_delete_file_email_invalid(self,mock_support_function, mock_user_repo):
        user_id = "1"
        email = "201333"
        name_file = "test1.pdf"
        mock_user_repo.getEmailUserByIdFix.return_value = (email,)
        request = RequestDeleteFile(user_id=user_id,name_file=name_file)
        response = deleteFile(request)
        self.assertIsInstance(response, res1.ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data, res.Message(message='Email invalid'))
    
    @patch('service.FileService.UserRepository.getEmailUserByIdFix')
    @patch('service.FileService.sf_dropbox.delete_file')
    @patch('service.FileService.sf.check_email_service', return_value='example@example.com')
    def test_delete_file_server_error(self, mock_support_function, mock_delete_file,mock_user_repo):
        user_id = "1"
        name_file = "test1.pdf"
        mock_delete_file.side_effect = Exception("Some error")
        request = RequestDeleteFile(user_id=user_id,name_file=name_file)
        response = deleteFile(request)
        self.assertIsInstance(response, res.ReponseError)
        self.assertEqual(response.status, 500)
        self.assertEqual(response.data.message, f"delete {name_file} error")
    
    @patch('service.FileService.UserRepository')
    @patch('service.FileService.sf.check_email_service', return_value='example@example.com')
    def test_delete_file_namefile_empty(self,mock_support_function, mock_user_repo):
        user_id = "1"
        email = "201333@gmail.com"
        name_file = ""
        request = RequestDeleteFile(user_id=user_id,name_file=name_file)
        response = deleteFile(request)
        self.assertIsInstance(response, res.ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data, res.Message(message='Name file is empty'))

class TestDeleteAllFile(unittest.TestCase): 
    @patch('service.FileService.UserRepository')
    @patch('service.FileService.sf_dropbox.delete_all_files_in_folder',return_value = True)
    @patch('service.FileService.sf.check_email_service', return_value='example@example.com')
    def test_delete_all_file_success(self,mock_sf,mock_delete_folder,mock_user_repo):
        user_id = "1"
        email = 'example@example.com'
        request = RequestDeleteAllFile(user_id=user_id)
        response = deleteAllFile(request)
        self.assertIsInstance(response, res.ResponseDeleteAllFile)
        self.assertEqual(response.status, 200)
        self.assertEqual(response.data, res.Message(message='Delete all file success'))
    
    @patch('service.FileService.UserRepository')
    @patch('service.FileService.sf.check_email_service', return_value=res.ReponseError(status=400, data=res.Message(
        message="Id not exist")))
    def test_delete_all_file_id_not_exist(self,mock_sf,mock_user_repo):
        user_id = "1"
        request = RequestDeleteAllFile(user_id=user_id)
        response = deleteAllFile(request)
        self.assertIsInstance(response, res.ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data, res.Message(message='Id not exist'))
    
    @patch('service.FileService.UserRepository')
    @patch('service.FileService.sf.check_email_service', return_value=res.ReponseError(status=400, data=res.Message(
        message="Email is empty")))
    def test_delete_all_file_email_empty(self,mock_sf,mock_user_repo):
        user_id = "1"
        email = None
        mock_user_repo.getEmailUserByIdFix.return_value = (email,)
        request = RequestDeleteAllFile(user_id=user_id)
        response = deleteAllFile(request)
        self.assertIsInstance(response, res.ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data, res.Message(message='Email is empty'))
    
    @patch('service.FileService.UserRepository')
    @patch('service.FileService.sf.check_email_service', return_value=res.ReponseError(status=400, data=res.Message(
        message="Email invalid")))
    def test_delete_all_file_email_invalid(self, mock_sf, mock_user_repo):
        user_id = "1"
        email = "201333"
        request = RequestDeleteAllFile(user_id=user_id)
        response = deleteAllFile(request)
        self.assertIsInstance(response, res.ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data, res.Message(message='Email invalid'))
    
    @patch('service.FileService.UserRepository')
    @patch('service.FileService.sf_dropbox.delete_all_files_in_folder')
    @patch('service.FileService.sf.check_email_service', return_value="20133@gmail.com")
    def test_delete_all_file_server_err(self,mock_sf,mock_delete_folder,mock_user_repo):
        user_id = "1"
        mock_delete_folder.side_effect = Exception("Some error")
        request = RequestDeleteAllFile(user_id=user_id)
        response = deleteAllFile(request)
        self.assertIsInstance(response, res.ReponseError)
        self.assertEqual(response.status, 500)
        self.assertEqual(response.data, res.Message(message='Delete all file error'))

class TestListNameFiles(unittest.TestCase):
    @patch('service.FileService.UserRepository')
    @patch('service.FileService.sf_dropbox.list_files')
    @patch('service.FileService.sf.check_email_service', return_value="20133118@gmail.com")
    def test_list_name_file_success(self,mock_sf, mock_list_files, mock_user_repo):
        user_id = "1"
        email = "quangphuc@gmail.com"
        list_files = [
            'demo1.pdf', 'CV_VoNhuY_Java.pdf', 'VanHoangLuong_DangXuanBach_TLCN.docx',
            'THÔNG-TIN-TUYỂN-DỤNG-Java.pdf', 'baitap_qlpv_nhom14.docx', 'PMBOK2012-5rd Edition.pdf',
            'BaoCaoThucTapTotnghiep_20133059_Fpt_Software.docx'
        ]
        mock_list_files.return_value = list_files
        request = RequestGetNameFile(user_id=user_id)
        response = listNameFiles(request)
        self.assertIsInstance(response, res.ResponseGetNameFile)
        self.assertEqual(response.status, 200)
        self.assertEqual(response.data.files, list_files)
        self.assertEqual(len(response.data.files), 7)
    
    @patch('service.FileService.UserRepository.getEmailUserByIdFix')
    @patch('service.FileService.sf_dropbox.list_files')
    @patch('service.FileService.sf.check_email_service', side_effect=Exception("Some error"))
    def test_listNameFiles_server_error(self, mock_sf, mock_list_files, mock_getEmailUserByIdFix):
        request = RequestGetNameFile(user_id="1")
        response = listNameFiles(request)
        self.assertEqual(response.status, 500)
        self.assertEqual(response.data.message, "Server Error")

    @patch('service.FileService.UserRepository')
    @patch('service.FileService.sf.check_email_service', return_value=res1.ReponseError(status=400, data=res.Message(
        message="Id not exist")))
    def test_list_name_files_id_not_exist(self, mock_sf, mock_user_repo):
        user_id = "1"
        email = 'example@example.com'
        name_file = "test1.pdf"
        request = RequestGetNameFile(user_id=user_id)
        response = listNameFiles(request)
        self.assertIsInstance(response, res1.ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data, res1.Message(message='Id not exist'))
    
    @patch('service.FileService.UserRepository')
    @patch('service.FileService.sf.check_email_service', return_value=res1.ReponseError(status=400, data=res.Message(
        message="Email is empty")))
    def test_list_name_files_email_empty(self,mock_sf, mock_user_repo):
        user_id = "1"
        email = None
        name_file = "test1.pdf"
        request = RequestGetNameFile(user_id=user_id)
        response = listNameFiles(request)
        self.assertIsInstance(response, res1.ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data, res.Message(message='Email is empty'))
    
    @patch('service.FileService.UserRepository')
    @patch('service.FileService.sf.check_email_service', return_value=res1.ReponseError(status=400, data=res.Message(
        message="Email invalid")))
    def test_list_name_files_email_invalid(self, mock_sf, mock_user_repo):
        user_id = "1"
        email = "201333"
        name_file = "test1.pdf"
        mock_user_repo.getEmailUserByIdFix.return_value = (email,)
        request = RequestGetNameFile(user_id=user_id)
        response = listNameFiles(request)
        self.assertIsInstance(response, res1.ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data, res.Message(message='Email invalid'))

class TestDownLoadFolder(unittest.TestCase):
    @patch('service.FileService.UserRepository')
    @patch('service.FileService.sf.check_email_service',return_value="example@example.com")
    def test_download_folder_success(self,mock_sf, mock_user_repo):
        user_id = "1"
        email = 'example@example.com'
        request = RequestDownLoadFolder(user_id=user_id)
        response = download_folder(request)
        self.assertIsInstance(response, res.ResponseDownloadFolder)
        self.assertEqual(response.status, 200)
        self.assertEqual(response.data, res.Message(message=f'Downloaded folder {email} success'))
    
    @patch('service.FileService.UserRepository.getEmailUserByIdFix')
    @patch('service.FileService.sf_dropbox.download_folder')
    @patch('service.FileService.sf.check_email_service', return_value="example@gmail.com")
    def test_download_folder_server_error(self, mock_sf, mock_download_folder, mock_getEmailUserByIdFix):
        mock_download_folder.side_effect = Exception('Test exception')
        request = RequestDownLoadFolder(user_id= "1")
        response = download_folder(request)
        self.assertEqual(response.status, 500)
        self.assertEqual(response.data.message, "Server error")

    @patch('service.FileService.UserRepository')
    @patch('service.FileService.sf.check_email_service', return_value=res1.ReponseError(status=400, data=res.Message(
        message="Id not exist")))
    def test_download_folder_id_not_exist(self,mock_sf,mock_user_repo):
        user_id = "1"
        request = RequestDownLoadFolder(user_id=user_id)
        response = download_folder(request)
        self.assertIsInstance(response, res1.ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data, res1.Message(message='Id not exist'))
    
    @patch('service.FileService.UserRepository')
    @patch('service.FileService.sf.check_email_service', return_value=res1.ReponseError(status=400, data=res.Message(
        message="Email is empty")))
    def test_download_folder_email_empty(self,mock_sf, mock_user_repo):
        user_id = "1"
        email = None
        mock_user_repo.getEmailUserByIdFix.return_value = (email,)
        request = RequestDownLoadFolder(user_id=user_id)
        response = download_folder(request)
        self.assertIsInstance(response, res1.ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data, res.Message(message='Email is empty'))
    
    @patch('service.FileService.UserRepository')
    @patch('service.FileService.sf.check_email_service', return_value=res1.ReponseError(status=400, data=res.Message(
        message="Email invalid")))
    def test_download_folder_email_invalid(self,mock_sf, mock_user_repo):
        user_id = "1"
        email = "201333"
        mock_user_repo.getEmailUserByIdFix.return_value = (email,)
        request = RequestDownLoadFolder(user_id=user_id)
        response = download_folder(request)
        self.assertIsInstance(response, res1.ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data, res1.Message(message='Email invalid'))

class TestDownLoadFile(unittest.TestCase):
    @patch('service.FileService.UserRepository')
    @patch('service.FileService.sf.check_email_service', return_value="quangphuc@gmail.com")
    def test_download_file_success(self, mock_sf, mock_user_repo):
        user_id = "1"
        email = "quangphuc@gmail.com"
        name_file = "demo1.pdf"
        request = RequestDownLoadFile(user_id=user_id,name_file=name_file)
        response = download_file(request)
        self.assertIsInstance(response, res.ResponseDownloadFile)
        self.assertEqual(response.status, 200)
        self.assertEqual(response.data, res.Message(message=f"Downloaded file '{name_file}' by email: '{email}' success"))
    
    @patch('service.FileService.UserRepository')
    @patch('service.FileService.sf.check_email_service', return_value=res1.ReponseError(status=400, data=res.Message(
        message="Id not exist")))
    def test_download_file_id_not_exist(self, mock_sf,mock_user_repo):
        user_id = "1"
        email = "quangphuc@gmail.com"
        name_file = "demo1.pdf"
        request = RequestDownLoadFile(user_id=user_id,name_file=name_file)
        response = download_file(request)
        self.assertIsInstance(response, res1.ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data, res.Message(message='Id not exist'))
    
    @patch('service.FileService.UserRepository')
    @patch('service.FileService.sf.check_email_service', return_value=res1.ReponseError(status=400, data=res.Message(
        message="Email is empty")))
    def test_download_file_email_empty(self,mock_sf, mock_user_repo):
        user_id = "1"
        email = None
        name_file = "demo1.pdf"
        request = RequestDownLoadFile(user_id=user_id,name_file=name_file)
        response = download_file(request)
        self.assertIsInstance(response, res1.ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data, res1.Message(message='Email is empty'))
    
    @patch('service.FileService.UserRepository')
    @patch('service.FileService.sf.check_email_service', return_value=res1.ReponseError(status=400, data=res.Message(
        message="Email invalid")))
    def test_download_file_email_invalid(self, mock_sf, mock_user_repo):
        user_id = "1"
        email = "201333"
        name_file = "demo1.pdf"
        request = RequestDownLoadFile(user_id=user_id,name_file=name_file)
        response = download_file(request)
        self.assertIsInstance(response, res1.ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data, res.Message(message='Email invalid'))
    
    @patch('service.FileService.UserRepository')
    @patch('service.FileService.sf.check_email_service', return_value="20133@gmail.com")
    def test_download_file_name_file_empty(self,mock_sf, mock_user_repo):
        user_id = "1"
        email = "201333@gmail.com"
        name_file = ""
        mock_user_repo.getEmailUserByIdFix.return_value = (email,)
        request = RequestDownLoadFile(user_id=user_id,name_file=name_file)
        response = download_file(request)
        self.assertIsInstance(response, res.ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data, res.Message(message='name_file is empty'))
    
    @patch('service.FileService.UserRepository.getEmailUserByIdFix')
    @patch('service.FileService.sf_dropbox.search_and_download_file')
    @patch('service.FileService.sf.check_email_service', return_value="20133@gmail.com")
    def test_download_file_server_error(self,mock_sf, mock_search_and_download_file, mock_getEmailUserByIdFix):
        # mock_getEmailUserByIdFix.side_effect = Exception('Test exception')
        mock_search_and_download_file.side_effect = Exception('Test exception')
        request = RequestDownLoadFile(user_id= "1",name_file="test1.txt")
        response = download_file(request)
        self.assertEqual(response.status, 500)
        self.assertEqual(response.data.message, "Server error")

class TestUploadFileService(unittest.TestCase):
    @patch('service.FileService.UserRepository')
    @patch('service.FileService.sf.check_email_service', return_value=res1.ReponseError(status=400, data=res.Message(
        message="Email invalid")))
    def test_upload_files_invalid_email(self, mock_sf, mock_user_repo):
        user_id = "1"
        email = "20133118"
        request = RequestUploadFile(user_id=user_id, files=[])
        response = upload_files(request)
        self.assertIsInstance(response, res1.ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message, "Email invalid")
    
    @patch('service.FileService.UserRepository')
    @patch('service.FileService.sf.check_email_service', return_value=res1.ReponseError(status=400, data=res.Message(
        message="Email is empty")))
    def test_upload_files_empty_email(self, mock_sf, mock_user_repo):
        user_id = "1"
        email = None
        request = RequestUploadFile(user_id=user_id, files=[])
        response = upload_files(request)
        self.assertIsInstance(response, res1.ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message, "Email is empty")
    
    @patch('service.FileService.UserRepository')
    @patch('service.FileService.sf.check_email_service', return_value=res1.ReponseError(status=400, data=res.Message(
        message="Id not exist")))
    def test_upload_files_id_not_exist(self, mock_sf, mock_user_repo):
        user_id = "1"
        email = 'mang1@gmail.com'
        mock_user_repo.getEmailUserByIdFix.return_value = None
        request = RequestUploadFile(user_id=user_id, files=[])
        response = upload_files(request)
        self.assertIsInstance(response, res1.ReponseError)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.data.message, "Id not exist")

    @patch('service.FileService.sf_dropbox.upload_file')
    @patch('service.FileService.UserRepository.getEmailUserByIdFix')
    @patch('service.FileService.allowed_file')
    @patch('service.FileService.check_email')
    @patch('service.FileService.os.makedirs')
    @patch('service.FileService.sf.check_email_service', return_value="mang1@gmail.com")
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_upload_files_success(self, mock_open,mock_sf, mock_makedirs, mock_check_email, mock_allowed_file, mock_get_email_user_by_id, mock_upload_file):
        user_id = "1"
        email = 'mang1@gmail.com'
        mock_get_email_user_by_id.return_value = (email,)
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
            request = RequestUploadFile(user_id=user_id, files=[file])
            mock_makedirs.side_effect = lambda path, exist_ok: None
            response = upload_files(request)
            self.assertIsInstance(response, res.ResponseUploadedFile)
            self.assertEqual(response.status, 200)
            self.assertEqual(response.data.message, "Load file success")
            # Adjust the expected call to match the actual call
            expected_src_path = os.path.join("/code/temp", email, file.filename).replace("\\", "/")
            expected_dst_path = f"/{email}/{file.filename}"
            actual_src_path, actual_dst_path = mock_upload_file.call_args[0]
            actual_src_path = actual_src_path.replace("\\", "/")
            print(actual_dst_path)
            print(actual_src_path)
            assert expected_src_path == actual_src_path and expected_dst_path == actual_dst_path

    @patch('service.FileService.sf_dropbox.upload_file')
    @patch('service.FileService.UserRepository.getEmailUserByIdFix')
    @patch('service.FileService.allowed_file')
    @patch('service.FileService.check_email')
    @patch('service.FileService.os.makedirs')
    @patch('service.FileService.shutil.copyfileobj')
    @patch('service.FileService.sf.check_email_service', return_value="mang1@gmail.com")
    def test_upload_files_invalid_file_type(self,mock_sf, mock_copyfileobj, mock_makedirs, mock_check_email, mock_allowed_file, mock_get_email_user_by_id, mock_upload_file):
        user_id = "1"
        email = 'mang1@gmail.com'
        mock_get_email_user_by_id.return_value = (email,)
        mock_check_email.return_value = True
        mock_allowed_file.return_value = False
        file_content = b"Test file content"
        file = UploadFile(filename='test.exe', file=BytesIO(file_content))
        request = RequestUploadFile(user_id=user_id, files=[file])
        response = upload_files(request)
        self.assertIsInstance(response, res.ReponseError)
        self.assertEqual(response.status, 415)
        self.assertEqual(response.data.message, "File type not allow")
        mock_upload_file.assert_not_called()
    
    @patch('service.FileService.UserRepository.getEmailUserByIdFix')
    @patch('service.FileService.sf_dropbox.upload_file')
    @patch('service.FileService.sf.check_email_service', return_value="test_email@example.com")
    def test_upload_files_error_handling(self,mock_sf, mock_upload_file, mock_getEmailUserByIdFix):
        mock_upload_file.side_effect = Exception('Test exception')
        request = MagicMock()
        request.user_id = "1"
        request.files = [
            MagicMock(filename='test_file.txt', file=MagicMock())
        ]
        response = upload_files(request)
        self.assertEqual(response.status, 500)
        self.assertEqual(response.data.message, "Load file error")


if __name__ == '__main__':
    unittest.main()