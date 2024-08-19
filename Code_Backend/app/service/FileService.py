from request import RequestFile as req
from response import ResponseFile as res
from response import ResponseDefault as res1
import function.dropbox as sf_dropbox
import os
import shutil
import re
from repository import UserRepository
from function import  support_function as sf
ALLOWED_EXTENSIONS = {'csv', 'txt', 'doc', 'docx', 'pdf', 'xlsx', 'pptx', 'json','md'}
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

def check_email(email):
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

async def listNameFiles(request: req.RequestGetNameFile ):
  try:
    user_id = request.user_id
    email = sf.check_email_service(user_id)
    if isinstance(email,res1.ReponseError):
        return email
    list_files = sf_dropbox.list_files(email)
    return res.ResponseGetNameFile(
       status= 200,
       data = res.DataGetNameFile(files=list_files)
    )
  except:
      return res.ReponseError(
            status=500,
            data =res.Message(message="Server Error")
        )

async def deleteFile(request: req.RequestDeleteFile):
  try:
   user_id = request.user_id
   name_file = request.name_file
   email = sf.check_email_service(user_id)
   if isinstance(email, res1.ReponseError):
        return email
   if name_file is None or name_file == "":
        return res.ReponseError(
            status=400,
            data =res.Message(message="Name file is empty")
        )
   sf_dropbox.delete_file(email,name_file)
   return res.ResponseDeleteFile(
            status=200,
            data =res.Message(message=f"delete {name_file} success")
        )
  except:
       return res.ReponseError(
            status=500,
            data =res.Message(message=f"delete {name_file} error")
        )

async def download_folder(request:req.RequestDownLoadFolder):
   try:
       user_id = request.user_id
       email = sf.check_email_service(user_id)
       if isinstance(email, res1.ReponseError):
           return email
       sf_dropbox.download_folder(email)
       return res.ResponseDownloadFolder(
            status=200,
            data =res.Message(message=f"Downloaded folder {email} success")
        )
   except: 
      return res.ReponseError(
            status=500,
            data =res.Message(message=f"Server error")
        )

async def download_file(request:req.RequestDownLoadFile):
   try:
       user_id = request.user_id
       name_file = request.name_file
       email = sf.check_email_service(user_id)
       if isinstance(email, res1.ReponseError):
           return email
       if name_file is None or name_file == "":
        return res.ReponseError(
            status=400,
            data =res.Message(message="name_file is empty")
        )
       sf_dropbox.search_and_download_file(name_file,email)
       return res.ResponseDownloadFile(
            status=200,
            data =res.Message(message=f"Downloaded file '{name_file}' by email: '{email}' success")
        )
   except: 
      return res.ReponseError(
            status=500,
            data =res.Message(message=f"Server error")
        )

ALLOWED_EXTENSIONS = {'csv', 'txt', 'doc', 'docx', 'pdf', 'xlsx', 'pptx', 'json','md'}

def allowed_file1(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
async def upload_files(request: req.RequestUploadFile):
 try:
   user_id = request.user_id
   files = request.files
   email = sf.check_email_service(user_id)
   if isinstance(email, res1.ReponseError):
       return email
   for file in files:
            if not allowed_file(file.filename):
                return res.ReponseError(
            status=415,
            data =res.Message(message=f"File type not allow")
        )
            temp_dir = f"/code/temp/{email}"
            os.makedirs(temp_dir, exist_ok=True)
            file_path = os.path.join(temp_dir, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            cloud_path = f"/{email}/{file.filename}"
            sf_dropbox.upload_file(file_path, cloud_path)
   return res.ResponseUploadedFile(
            status=200,
            data =res.Message(message=f"Load file success")
        )
 except:
    return res.ReponseError(
            status=500,
            data =res.Message(message=f"Load file error")
        )

async def deleteAllFile(request: req.RequestDeleteAllFile):
 try:
    user_id = request.user_id
    email = sf.check_email_service(user_id)
    if isinstance(email, res.ReponseError):
        return email
    sf_dropbox.delete_all_files_in_folder(email)
    return res.ResponseDeleteAllFile(
            status=200,
            data=res.Message(message=f"Delete all file success")
        )
 except:
     return res.ReponseError(
            status=500,
            data=res.Message(message=f"Delete all file error")
        )
