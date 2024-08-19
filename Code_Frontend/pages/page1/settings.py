import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from streamlit_cookies_controller import CookieController
import time,requests
from dotenv import load_dotenv
from pages.page1 import support_function as sf
import os
import json

def show_settings():
 st.header("Chat Settings", divider='green')
 load_dotenv()
 API = os.getenv("BE_API")
 api = API
 controller = CookieController()
 token = controller.get('token_data')
 session_id_now = controller.get('session_id')
 
 def get_message(result):
   res = result.json()['data']
   message = res["message"]
   return message
 
 import datetime
 if token:  
            sf.check_time_token(token)
            picture_user = ""
            url = f"{api}/default/is_me"
            response = requests.get(url,params={'token': token})
            if response.status_code == 422:
                            message = "Unprocessable Entity"
                            st.toast(f"{message}", icon='❌')
            elif response.status_code == 500:
                            message = "Internal Server Error"
                            st.toast(f"{message}", icon='❌')
            elif response.status_code == 404:
                            message = "Not found"
                            st.toast(f"{message}", icon='❌')
            elif response.status_code == 502:
                            message = "Bad Gateway"
                            st.toast(f"{message}", icon='❌')
            elif response.json()['status'] != 200:
                 message = response.json()['data']['message']
                 st.toast(message, icon='❌')
            res_status = response.json()['status']
            res = response.json()['data']
            if res_status == 200:
                user_id = res["user_id"]
                st.session_state["user_id"] = 0
                st.session_state["user_id"]  = user_id
                headers = {"Authorization": f"Bearer {token}",'Content-Type': 'application/json', 'accept': 'application/json'}
                url_info = f"{api}/default/info_user/{user_id}"
                user_info_data = requests.get(url_info, headers=headers)
                if user_info_data.status_code == 422:
                            message = "Unprocessable Entity"
                            st.toast(f"{message}", icon='❌')
                elif response.status_code == 502:
                            message = "Bad Gateway"
                elif user_info_data.status_code == 500:
                            message = "Internal Server Error"
                            st.toast(f"{message}", icon='❌')
                elif user_info_data.status_code == 404:
                            message = "Not found"
                            st.toast(f"{message}", icon='❌')
                user_info_status = user_info_data.json()['status']
                if user_info_status != 200:
                  message = user_info_data.json()['data']['message']
                  st.toast(message, icon='❌')
                res1 = user_info_data.json()['data']
                if user_info_status == 500:
                    st.toast("Error",icon='❌')
                elif user_info_status == 502:
                  message = "Bad Gateway"
                  st.toast(message, icon='❌')
                res1 = user_info_data.json()['data']              
                picture_user = res1["photo_url"]
                st.session_state['current_photo_url'] = ""
                st.session_state['current_photo_url'] = picture_user
                st.session_state["name_user"] = ""
                st.session_state["name_user"] = res1["display_name"]
                st.session_state["uid"] = ""
                st.session_state["uid"]  = res1["uid"]
                st.session_state["email"] = ""
                st.session_state["email"]  = res1["email"]
 def upload_files_to_api(api_endpoint, uploaded_files):
    if uploaded_files:
        token = st.session_state["token"]
        headers = {"Authorization": f"Bearer {token}", 'accept': 'application/json'}
        user_id = st.session_state["user_id"]

        def process_file(file):
            file_data = file.read()
            files = {"files": (file.name, file_data, file.type)}

            response = requests.post(api_endpoint, files=files, data={'user_id': user_id}, headers=headers)
            if response.status_code == 403:
                sf.refresh_token_account()
                token = st.session_state["token"]
                headers["Authorization"] = f"Bearer {token}"
                response = requests.post(api_endpoint, files=files, data={'user_id': user_id}, headers=headers)
            return response

        for file in uploaded_files:
            response = process_file(file)
            if not sf.check_status_response(response):
                return

            status = response.json()['status']
            if status == 200:
                message = get_message(response)
                st.toast(message, icon='✅')
                download_url = f"{api}/file/chatbot/download_folder"
                download_folder_response = requests.post(download_url, json={'user_id': user_id}, headers=headers)
                if download_folder_response.status_code == 403:
                    sf.refresh_token_account()
                    token = st.session_state["token"]
                    headers["Authorization"] = f"Bearer {token}"
                    download_folder_response = requests.post(download_url, json={'user_id': user_id}, headers=headers)
                if not sf.check_status_response(download_folder_response):
                    return
                # Extract file
                extract_url = f"{api}/chat/chatbot/extract_file/{user_id}"
                extract_response = requests.get(extract_url, headers=headers)
                if extract_response.status_code == 403:
                    sf.refresh_token_account()
                    token = st.session_state["token"]
                    headers["Authorization"] = f"Bearer {token}"
                    extract_response = requests.get(extract_url, params={'user_id': user_id}, headers=headers)
                if not sf.check_status_response(extract_response):
                    return
                if extract_response.status_code == 200:
                    text_all = extract_response.json()['data']['text_all']
                    res = json.dumps(text_all)
                    st.session_state["text_all"] = res
                # Generate question
                api_generate_question = f"{api}/chat/chatbot/generate_question/{user_id}"
                question_response = requests.get(api_generate_question, headers=headers)
                if question_response.status_code == 403:
                    sf.refresh_token_account()
                    token = st.session_state["token"]
                    headers["Authorization"] = f"Bearer {token}"
                    question_response = requests.get(api_generate_question, headers=headers)
                if not sf.check_status_response(question_response):
                    return
                if question_response.status_code == 200:
                    question = question_response.json()['data']['question']
                    st.session_state["generate_question"] = question
                    st.toast("Generate question success", icon='✅')
            elif status in (400, 500, 404):
                message = get_message(response)
                st.toast(message, icon='❌')
            elif response.status_code == 502:
                st.toast("Bad Gateway", icon='❌')
    else:
        st.toast("No files have been uploaded yet.", icon='❌')
 def display_file_list():
    def get_file_list():
        api_getfile = f"{api}/file/list_name_files"
        token = st.session_state["token"]
        headers = {
            "Authorization": f"Bearer {token}",
            'accept': 'application/json'
        }
        parameters = {
            'user_id': st.session_state["user_id"]
        }
        return requests.get(api_getfile, params=parameters, headers=headers)
    response = get_file_list()  
    if response.status_code == 403:
        sf.refresh_token_account()
        response = get_file_list()
    if not sf.check_status_response(response):
        return 
    status = response.json().get('status', 500)
    result = response.json().get('data', {}) 
    if status == 200:
        file_list = result.get("files", [])
        file_list = [file.strip().strip("'") for file in file_list]
        return file_list
    elif status == 400:
        message = get_message(response)
        st.toast(message, icon='❌')
    elif status == 404:
        message = get_message(response)
        st.toast(message, icon='❌')
    elif status == 500:
        message = get_message(response)
        st.toast(message, icon='❌')
    elif response.status_code == 502:
        st.toast("Bad Gateway", icon='❌')
 st.session_state["params"] = dict()
 st.session_state["params"]["uploaded_file"] = st.file_uploader(":blue[Upload your file]", type=['txt', 'csv', 'xlsx','doc','docx','pptx','pdf'], accept_multiple_files=True)
 with stylable_container(
           "loadfile",
         css_styles="""
          button {
           background-color: #2ECC71 ;
           color: white;
           border-radius: 7px;
           }""",
        ):
           btnLoadFile= st.button("📑 Load File", key="btnloadfile",use_container_width=True)
 if btnLoadFile:
            api_endpoint = f"{api}/file/upload_files"
            uploaded_files = st.session_state.get("params", {}).get("uploaded_file", [])
            if uploaded_files:
                valid_files = []
                for uploaded_file in uploaded_files:
                        valid_files.append(uploaded_file)
                if valid_files:
                    upload_files_to_api(api_endpoint, valid_files)
                else:
                    st.toast("No valid file uploaded.", icon='❌')
            else:
                st.toast("No file uploaded yet.", icon='❌')
 import pandas as pd
 file_list = display_file_list()
 st.session_state["params"]["list_file"] = st.selectbox(":blue[Select a File]", file_list)
 file_name = st.session_state["params"]["list_file"]
 st.write(f"You select file: {file_name}")
 with stylable_container(
           "deletefile",
         css_styles="""
          button {
           background-color: #DE3163 ;
           color: white;
           border-radius: 7px;
           }""",
        ):
           btnDelete = st.button("❌ Delete File",use_container_width=True)
 if btnDelete and file_name:
                user_id = st.session_state["user_id"]
                token = st.session_state["token"]
                api_deletefile = f"{api}/file/delete_file"
                parameters2 = {
        'user_id': st.session_state["user_id"],
        'name_file': file_name
    }           
                headers = {
         "Authorization": f"Bearer {token}",
         'accept': 'application/json',
         'Content-Type': 'application/json'   
          }
                response = requests.delete(api_deletefile, json=parameters2,headers=headers)
                if not sf.check_status_response(response):
                  return
                status = response.json()['status']
                data = response.json()['data']
                if status == 200:
                    result1 = get_message(response)
                    file_list1 = display_file_list()
                    st.session_state["params"]["list_file"] = file_list1
                    headers = {
               "Authorization": f"Bearer {token}",    
                  }
                    params = {'user_id': st.session_state["user_id"],}
                    url1 = f"{api}/file/chatbot/download_folder"
                    requests.post(url1,json=params,headers=headers)
                    api_generate_question = f"{api}/chat/chatbot/generate_question/{user_id}"
                    response_generate_question = requests.get(api_generate_question, headers=headers)
                    if not sf.check_status_response(response_generate_question):
                       return
                    elif response_generate_question.status_code == 403:
                         sf.refresh_token_account()
                         token = st.session_state["token"]
                         headers = {"Authorization": f"Bearer {token}",}     
                         response_generate_question = requests.get(api_generate_question, headers=headers)
                         question = response_generate_question.json()['data']['question']
                         st.session_state["generate_question"] = question
                         st.toast("Generate question success", icon='✅')
                    status_question= response.json()['status']
                    if status_question == 200:
                        question = response_generate_question.json()['data']['question']
                        st.session_state["generate_question"] = question
                        st.toast("Generate question success", icon='✅')
                    user_id = st.session_state["user_id"]
                    api_endpoint = f"{api}/chat/chatbot/extract_file/{user_id}"
                    response1 = requests.get(api_endpoint, headers=headers)
                    if not sf.check_status_response(response1):
                            return
                    status_res1 = response1.json()['status']
                    # status_data1 = response1.json()['data']
                    if status_res1 == 200:
                      st.session_state["text_all"] = ""
                      text_all = response1.json()['data']['text_all']
                      res = json.dumps(text_all)
                      st.session_state["text_all"] = res
                      st.toast("Extract data success", icon='✅')
                    st.toast(result1, icon='✅')
                elif status == 400:
                   message = get_message(response)
                   st.toast(message, icon='❌')
                elif status == 404:
                   message = get_message(response)
                   st.toast(message, icon='❌')
                elif status == 500:
                    message = get_message(response)
                    st.toast(message, icon='❌')
                elif response.status_code == 403:
                    sf.refresh_token_account()
                    token = st.session_state["token"]
                    headers = {
         "Authorization": f"Bearer {token}"         
          }
                    requests.delete(api_deletefile,json=parameters2,headers=headers)
                    st.toast("Delete file success", icon='✅')
 with stylable_container(
           "deletefile",
         css_styles="""
          button {
           background-color: #DE3163 ;
           color: white;
           border-radius: 7px;
           }""",
        ):
           btnDelete_All = st.button("❌ Delete All File",use_container_width=True)
 if btnDelete_All:
                token = st.session_state["token"]
                api_delete_all_file = f"{api}/file/delete"
                parameters3 = {
        'user_id': st.session_state["user_id"]
    }           
                headers1 = {
         "Authorization": f"Bearer {token}",
         'accept': 'application/json',
         'Content-Type': 'application/json'   
          }
                response = requests.delete(api_delete_all_file, json=parameters3, headers=headers1)
                if not sf.check_status_response(response):
                    return
                status = response.json()['status']
                if response.status_code == 403:
                    sf.refresh_token_account()
                    token = st.session_state["token"]
                    data = {'user_id': st.session_state["user_id"]}           
                    headers = {
                      "Authorization": f"Bearer {token}",
                      'accept': 'application/json',
                      'Content-Type': 'application/json'   
                    }           
                    request_delete = requests.delete(api_delete_all_file,json=data,headers=headers)
                    if not sf.check_status_response(request_delete):
                        return
                    if request_delete.json()['status'] == 200:
                        st.toast("Delete all file success", icon='✅')
                if status == 200:
                    result1 = get_message(response)
                    file_list1 = display_file_list()
                    st.session_state["params"]["list_file"] = file_list1
                    headers = {
               "Authorization": f"Bearer {token}",    
                  }
                    params = { 'user_id': st.session_state["user_id"],}
                    url1 = f"{api}/file/chatbot/download_folder"
                    download_folder = requests.post(url1,json=params,headers=headers)
                    if not sf.check_status_response(download_folder):
                        return
                    elif download_folder.status_code == 403:
                          sf.refresh_token_account()
                          token = st.session_state["token"]
                          headers = {
               "Authorization": f"Bearer {token}",    
                  }
                          params = { 'user_id': st.session_state["user_id"],}
                          url1 = f"{api}/file/chatbot/download_folder/"
                          requests.post(url1,json=params,headers=headers)
                          st.toast("Download folder success", icon='✅')
                    user_id = st.session_state["user_id"]
                    api_endpoint = f"{api}/chat/chatbot/extract_file/{user_id}"
                    response1 = requests.get(api_endpoint, headers=headers)
                    if not sf.check_status_response(response1):
                            return
                    elif response1.status_code == 403:
                        sf.refresh_token_account()
                        user_id = st.session_state["user_id"]
                        api_endpoint = f"{api}/chat/chatbot/extract_file/{user_id}"
                        headers = {
               "Authorization": f"Bearer {token}",    
                        }
                        extract_file= requests.get(api_endpoint, headers=headers)
                        status_res1 = response1.json()['status']
                        if status_res1 == 200:
                          st.session_state["text_all"] = ""
                          text_all = response1.json()['data']['text_all']
                          res = json.dumps(text_all)
                          st.session_state["text_all"] = res
                          st.toast("Extract data success", icon='✅')
                    status_res1 = response1.json()['status']
                    if status_res1 == 200:
                      st.session_state["text_all"] = ""
                      text_all = response1.json()['data']['text_all']
                      res = json.dumps(text_all)
                      st.session_state["text_all"] = res
                      st.toast("Extract data success", icon='✅')
                    if status_res1 != 200:
                        message = response1.json()['data']['message']
                        st.toast(message,icon='❌')
                    st.toast(result1, icon='✅')
                elif status == 500:
                    message = get_message(response)
                    st.toast(message, icon='❌')
                elif status == 400:
                    message = get_message(response)
                    st.toast(message, icon='❌')
                elif status == 404:
                    message = get_message(response)
                    st.toast(message, icon='❌')
 st.write("List of documents:")
 df = pd.DataFrame(file_list, columns=["Files"])
 df.index = df.index + 1 
 df.index.name = "STT" 
 st.session_state["params"] = {"list_file": df}
 st.table(st.session_state["params"]["list_file"])