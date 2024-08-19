import dropbox.files
import os
import shutil
import requests, base64
from fastapi import HTTPException
from dotenv import load_dotenv
import os
load_dotenv()
DROPBOX_APP_KEY=os.getenv('DROPBOX_APP_KEY')
DROPBOX_APP_SECRET=os.getenv('DROPBOX_APP_SECRET')
DROPBOX_REFRESH_TOKEN=os.getenv('DROPBOX_REFRESH_TOKEN')

def refresh_token_dropbox():
    app_key = DROPBOX_APP_KEY
    app_secret = DROPBOX_APP_SECRET
    refresh_token = DROPBOX_REFRESH_TOKEN
    url = 'https://api.dropbox.com/oauth2/token'
    auth_string = f"{app_key}:{app_secret}"
    base64authorization = base64.b64encode(auth_string.encode()).decode('utf-8')
    headers = {
        'Authorization': f'Basic {base64authorization}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    }
    response = requests.post(url, headers=headers, data=data)
    response_json = response.json()
    access_token = response_json.get('access_token', None)
    return access_token

def delete_file(id,name_file):
    try:
        TOKEN = refresh_token_dropbox()
        dbx=dropbox.Dropbox(TOKEN)
        file_path = f"/{id}/{name_file}"
        dbx.files_delete_v2(file_path)
        print(f"Xóa file '{file_path}' thành công.")
    except dropbox.exceptions.ApiError as e:
        print(f"Lỗi khi xóa file '{file_path}': {e}")

def list_files(id):
    file_names = []
    try:
        TOKEN = refresh_token_dropbox()
        dbx=dropbox.Dropbox(TOKEN)
        result = dbx.files_list_folder(f"/{id}")
        for entry in result.entries:
            if isinstance(entry, dropbox.files.FileMetadata):
                file_names.append(os.path.basename(entry.path_display))
    except dropbox.exceptions.ApiError as e:
        print(f"Error listing files: {e}") 
    return file_names

def upload_file_fix(local_path,cloud_path,token):
    try:
        TOKEN = refresh_token_dropbox()
        dbx=dropbox.Dropbox(TOKEN)
        with open(local_path, "rb") as f:
            data = f.read()
        dbx.files_upload(data, cloud_path)
        print(f"Uploaded file '{local_path}' to '{cloud_path}'")
    except dropbox.exceptions.ApiError as e:
        print(f"Error uploading file '{local_path}': {e}")

def upload_file(local_path, cloud_path):
    try:
        TOKEN = refresh_token_dropbox()
        dbx=dropbox.Dropbox(TOKEN)
        with open(local_path, "rb") as f:
            data = f.read()
        dbx.files_upload(data, cloud_path)
        print(f"Uploaded file '{local_path}' to '{cloud_path}'")
    except dropbox.exceptions.ApiError as e:
        upload_file_fix()

def clear_local_folder(path):
    try:
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
    except Exception as e:
        print(f"Failed to delete contents of {path}. Reason: {e}")

def download_folder(id):
    try:
        TOKEN = refresh_token_dropbox()
        dbx = dropbox.Dropbox(TOKEN)
        local_path = f"./user_file/{id}"
        os.makedirs(local_path, exist_ok=True)
        clear_local_folder(local_path)
        result = dbx.files_list_folder(f"/{id}")
        for entry in result.entries:
            if isinstance(entry, dropbox.files.FileMetadata):
                cloud_file_path = entry.path_display
                file_name = os.path.basename(cloud_file_path)
                local_file_path = os.path.join(local_path, file_name)
                dbx.files_download_to_file(local_file_path, cloud_file_path)
                print(f"Downloaded file '{file_name}' to '{local_file_path}'")
    except dropbox.exceptions.ApiError as e:
        print(f"Error downloading file '{id}': {e}")

def download_file_id(file_name, id):
    try:
        TOKEN = refresh_token_dropbox()
        dbx = dropbox.Dropbox(TOKEN)
        local_folder_path = f"./user_file/{id}"
        os.makedirs(local_folder_path, exist_ok=True)
        local_file_path = os.path.join(local_folder_path, file_name)
        with open(local_file_path, "wb") as f:
            metadata, response = dbx.files_download(f"/{id}/{file_name}")
            f.write(response.content)
        print(f"Downloaded file '{file_name}' to '{local_file_path}'")
    except dropbox.exceptions.ApiError as e:
        print(f"Error downloading file '{file_name}': {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def search_and_download_file(start_char, id):
    try:
        TOKEN = refresh_token_dropbox()
        dbx = dropbox.Dropbox(TOKEN)
        result = dbx.files_list_folder(f"/{id}")
        files_starting_with_char = [entry.name for entry in result.entries if entry.name.startswith(start_char)]
        if len(files_starting_with_char) == 0:
            print(f"No file found starting with '{start_char}' in folder '{id}'")
            return
        file_name = files_starting_with_char[0]
        local_folder_path = f"./user_file/{id}"
        os.makedirs(local_folder_path, exist_ok=True)
        local_file_path = os.path.join(local_folder_path, file_name)
        with open(local_file_path, "wb") as f:
            metadata, response = dbx.files_download(f"/{id}/{file_name}")
            f.write(response.content)
        print(f"Downloaded file '{file_name}' to '{local_file_path}'")
    except dropbox.exceptions.ApiError as e:
        print(f"Error searching or downloading file: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def delete_all_files_in_folder(folder_id):
    try:
        TOKEN = refresh_token_dropbox()
        dbx = dropbox.Dropbox(TOKEN)
        result = dbx.files_list_folder(f"/{folder_id}")
        for entry in result.entries:
            if isinstance(entry, dropbox.files.FileMetadata):
                file_path = entry.path_display
                dbx.files_delete_v2(file_path)
                print(f"Deleted file '{file_path}'")
        print(f"All files in folder '{folder_id}' have been deleted.")
    except dropbox.exceptions.ApiError as e:
        print(f"Error deleting files: {e}")