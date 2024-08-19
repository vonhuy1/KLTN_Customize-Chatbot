from fastapi import APIRouter, Form, File, UploadFile,Query
from typing import List,Optional
from service import FileService
from function import support_function
from fastapi import HTTPException
from response import ResponseFile as res
from request import RequestFile
router = APIRouter()

ALLOWED_EXTENSIONS = {'csv', 'txt', 'doc', 'docx', 'pdf', 'xlsx', 'pptx', 'json', 'html'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@router.delete("/delete", tags=["File"])
async def delete_folder(request: RequestFile.RequestDeleteAllFile):
    check = support_function.check_value_user_id_controller(request.user_id)
    if check is not True:
        return check
    # request = RequestFile.RequestDeleteAllFile(user_id=user_id)
    return  await FileService.deleteAllFile(request)

@router.get("/list_name_files", tags=["File"])
async def get_name(user_id: str):
    check = support_function.check_value_user_id_controller(user_id)
    if check is not True:
        return check
    request = RequestFile.RequestGetNameFile(user_id=user_id)
    return await FileService.listNameFiles(request)

@router.delete("/delete_file", tags=["File"])
async def delete_one_file(request: RequestFile.RequestDeleteFile):
    user_id = request.user_id
    check = support_function.check_value_user_id_controller(user_id)
    if check is not True:
        return check
    name_file = request.name_file
    if name_file is None or name_file.strip() == "":
        return res.ReponseError(status=400,
                                data=res.Message(message="Name file is required."))
    return await FileService.deleteFile(request)

@router.post("/chatbot/download_folder", tags=["File"])
async def download_folder_from_dropbox(request: RequestFile.RequestDownLoadFolder):
    user_id = request.user_id
    check = support_function.check_value_user_id_controller(user_id)
    if check is not True:
        return check
    return await FileService.download_folder(request)

@router.post("/chatbot/download_files", tags=["File"])
async def download_file_by_id(request: RequestFile.RequestDownLoadFile):
    user_id = request.user_id
    check = support_function.check_value_user_id_controller(user_id)
    if check is not True:
        return check
    return await FileService.download_file(request)

@router.post("/upload_files", tags=["File"])
async def upload_files_dropbox(user_id: str = Form(None), files: Optional[List[UploadFile]] = File(None)):
    check = support_function.check_value_user_id_controller(user_id)
    if check is not True:
        return check
    request = RequestFile.RequestUploadFile(files=files, user_id=user_id)
    return await FileService.upload_files(request)