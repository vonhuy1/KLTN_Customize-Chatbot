from dotenv import load_dotenv
import os   
load_dotenv()
API = os.getenv("BE_API")

def show_home():
 from streamlit_cookies_controller import CookieController
 from pages.page1 import support_function as sf
 import time
 import streamlit as st
 from streamlit_extras.stylable_container import stylable_container
 from pages.page1.utils import render_footer
 from streamlit_mic_recorder import speech_to_text
 import requests
 import random
 import string
 api = API
 controller = CookieController()
 token = controller.get('token_data')
 login_google = controller.get('login_google')
 st.session_state["session_id"] = controller.get('session_id')
 st.session_state["login_google"] = ""
 st.session_state["login_google"] = login_google
 css = """
<style>
.st-emotion-cache-7xfda7 {
    display: inline-flex;
    -webkit-box-align: center;
    align-items: center;
    -webkit-box-pack: center;
    justify-content: center;
    font-weight: 400;
    padding: 0.25rem 0.75rem;
    border-radius: 0.5rem;
    min-height: 38.4px;
    margin: 0px;
    line-height: 1.6;
    width: 100%;
    user-select: none;
    background: -webkit-linear-gradient(#ff520b, #fdffd0);
    color: rgb(255, 255, 255);
    border: 1px solid #dc3545;
}
</style>
"""
 def get_message(result):
   res = result.json()['data']
   message = res["message"]
   return message
 import datetime
 
 if token:  
            sf.check_time_token(token)
            st.session_state["user_id"] = 0
            st.session_state["token"] = ""
            picture_user = ""
            url = f"{api}/default/is_me"
            response = requests.get(url,params={'token': token})
            if not sf.check_status_response(response):
                  return
            res_status = response.json()['status']
            res = response.json()['data']
            if res_status == 200:
                user_id = res["user_id"]
                st.session_state["user_id"] = user_id
                headers = {"Authorization": f"Bearer {token}",'Content-Type': 'application/json', 'accept': 'application/json'}
                url_info = f"{api}/default/info_user/{user_id}"
                user_info_data = requests.get(url_info,headers=headers)
                if not sf.check_status_response(user_info_data):
                       return
                if user_info_data.status_code == 403:
                    sf.refresh_token_account()
                    token = controller.get("token_data")
                    headers = {"Authorization": f"Bearer {token}",'Content-Type': 'application/json', 'accept': 'application/json'}
                    url_info = f"{api}/default/info_user/{user_id}"
                    user_info_data = requests.get(url_info,headers=headers)
                    if not sf.check_status_response(user_info_data):
                        return
                    user_info_status = user_info_data.json()['status']
                    res1 = user_info_data.json()['data']
                    if user_info_status == 404:
                      message = user_info_data.json()['data']['message']
                      st.toast(message,icon='❌')
                    if user_info_status == 400:
                       message = user_info_data.json()['data']['message']
                       st.toast(message,icon='❌')
                    if user_info_status == 500:
                      message = user_info_data.json()['data']['message']
                      st.toast(message,icon='❌')
                    elif user_info_status == 502:
                      message = "Bad Gateway"
                      st.toast(message, icon='❌')
                    res1 = user_info_data.json()['data']              
                    picture_user = res1["photo_url"]
                    st.session_state['current_photo_url'] = ""
                    st.session_state['current_photo_url'] = picture_user
                    st.session_state["name_user"] = res1["display_name"]
                    st.session_state["uid"] = ""
                    st.session_state["uid"]  = res1["uid"]
                    st.session_state["email"] = ""
                    st.session_state["email"]  = res1["email"]
                    st.session_state["token"] = token
  
                user_info_status = user_info_data.json()['status']
                res1 = user_info_data.json()['data']
                if user_info_status == 404:
                    message = user_info_data.json()['data']['message']
                    st.toast(message,icon='❌')
                if user_info_status == 400:
                    message = user_info_data.json()['data']['message']
                    st.toast(message,icon='❌')
                if user_info_status == 500:
                    message = user_info_data.json()['data']['message']
                    st.toast(message,icon='❌')
                elif user_info_status == 502:
                  message = "Bad Gateway"
                  st.toast(message, icon='❌')
                res1 = user_info_data.json()['data']              
                picture_user = res1["photo_url"]
                st.session_state['current_photo_url'] = ""
                st.session_state['current_photo_url'] = picture_user
                st.session_state["name_user"] = res1["display_name"]
                st.session_state["uid"] = ""
                st.session_state["uid"]  = res1["uid"]
                st.session_state["email"] = ""
                st.session_state["email"]  = res1["email"]
                st.session_state["token"] = token
            else:
                message = response.json()['data']['message']
                st.toast(f"{message}", icon='❌')
                
                
 st.markdown(css, unsafe_allow_html=True)

 css_12 = """
        <style>
         .st-emotion-cache-1jmvea6 p {
            word-break: break-word;
            margin-bottom: 0px;
            font-size: 16px;
            font-weight: bold;
}
        </style>
    """
 st.markdown(css_12, unsafe_allow_html=True)
 
 
         
 def init_session():
    token = controller.get('token_data')
    if token is None or token ==" ":
        time.sleep(1)
        message = "You are denied access. Please Login"
        st.toast(message, icon='❌')
        time.sleep(2)
        st.markdown('<meta http-equiv="refresh" content="0;URL= http://localhost:8501/login" />', unsafe_allow_html=True)
    if 'check_query' not in st.session_state:
        st.session_state["check_query"] = False
    if not st.session_state.get("params"):
        st.session_state["params"] = dict()
    if not st.session_state.get("call_handle_ask"):
        st.session_state["call_handle_ask"] = False
    if not st.session_state.get("chats"):
        st.session_state["chats"] = {}
    if "input" not in st.session_state:
        st.session_state["input"] = "Hello, this is a custom chatbot for documents!"
  
 def new_chat(chat_name):
    if not st.session_state["chats"].get(chat_name):
        st.session_state["chats"][chat_name] = {
            "answer": [],
            "question": [],
            "data_relevant": [],
            "source_file": [],
            "id": [],
            "messages": [
                {"role": "system", "content": "Hello, this is a custom chatbot for documents!"}
            ],
            "is_delete": False,
            "display_name": chat_name,
        }
    return chat_name

 def switch_chat(chat_name):
    if st.session_state.get("current_chat") != chat_name:
        st.session_state["current_chat"] = chat_name
        css = """
<style>
.st-emotion-cache-7xfda7 {
    display: inline-flex;
    -webkit-box-align: center;
    align-items: center;
    -webkit-box-pack: center;
    justify-content: center;
    font-weight: 400;
    padding: 0.25rem 0.75rem;
    border-radius: 0.5rem;
    min-height: 38.4px;
    margin: 0px;
    line-height: 1.6;
    width: 100%;
    user-select: none;
    background: -webkit-linear-gradient(#ff520b, #fdffd0);
    color: rgb(255, 255, 255);
    bborder: 1px solid #dc3545;
}
</style>
"""
        st.markdown(css, unsafe_allow_html=True)
        css_1 = """
        <style>
         .st-emotion-cache-1jmvea6 p {
            word-break: break-word;
            margin-bottom: 0px;
            font-size: 16px;
            font-weight: bold;
}
        </style>
    """
        st.markdown(css_1, unsafe_allow_html=True)
        render_chat(st.session_state["current_chat"])
        st.stop()

 def switch_chat_name(chat_name):
    if st.session_state.get("current_chat") != chat_name:
        st.session_state["current_chat"] = chat_name
        render_sidebar()
        render_chat(st.session_state["current_chat"])
        st.stop()

 def delete_chat(chat_name):
    current_chats = [chat for chat, value in st.session_state['chats'].items() if not value['is_delete']]
    if len(current_chats) == 0:
        switch_chat(new_chat(f"Chat{len(st.session_state['chats'])}"))
        st.stop()
    if st.session_state["current_chat"] == chat_name:
        url = f"{api}/mysql/chat_history/delete"
        payload = {'user_id': st.session_state["user_id"], 'chat_name': chat_name}
        token = controller.get("token_data")
        headers = {"Authorization": f"Bearer {token}", 'Content-Type': 'application/json', 'accept': 'application/json'}
        def call_api(url, payload, headers):
            response = requests.delete(url, json=payload, headers=headers)
            if not sf.check_status_response(response):
                return None
            elif response.status_code == 403:
                sf.refresh_token_account()
                token = st.session_state["token"]
                headers["Authorization"] = f"Bearer {token}"
                response = requests.delete(url, json=payload, headers=headers)
                if not sf.check_status_response(response):
                    return None
            return response
        response = call_api(url, payload, headers)
        if not response:
            return
        status = response.json().get('status')
        if status == 200:
            message = get_message(response)
            st.toast(f'{message}', icon='✅')
            if chat_name in st.session_state['chats']:
                   st.session_state['chats'][chat_name]['is_delete'] = True
            del st.session_state["current_chat"]
            if len(st.session_state["chats"]) == 0:
                    switch_chat(new_chat(f"Chat{len(st.session_state['chats_1'])}_NewChat"))
            elif len(st.session_state["chats"]) != 0: 
                current_chats = [chat for chat, value in st.session_state['chats'].items() if not value['is_delete']]
                if current_chats:
                    switch_chat_name(current_chats[-1])
        else:
            message = response.json()['data'].get('message', 'Unknown error')
            st.toast(f"{message}", icon='❌')
    
 def edit_chat(chat_name, zone):
    def edit():
        new_name = st.session_state.get('edited_name')
        if not new_name:
            st.toast("name is empty!", icon='❌')
            return
        if new_name != chat_name and new_name in st.session_state['chats']:
            st.toast("name is duplicated!", icon='❌')
            return 
        if new_name == chat_name:
            st.toast("name is not modified!", icon='❌')
            return
        def call_api(url, params=None, payload=None, method='get'):
            token = controller.get("token_data")
            headers = {
                "Authorization": f"Bearer {token}",
                'Content-Type': 'application/json',
                'accept': 'application/json'
            }
            if method == 'get':
                response = requests.get(url, params=params, headers=headers)
            else:
                response = requests.put(url, json=payload, headers=headers)
            
            if response.status_code == 403:
                sf.refresh_token_account()
                st.toast("Please try the function again", icon='❌')
                return None
            elif not sf.check_status_response(response):
                return None
            return response
        response = call_api(f"{api}/default/is_me", params={'token': controller.get('token_data')})
        if not response:
            return
        res = response.json().get('data', {})
        user_id = res.get("user_id")
        if not user_id:
            st.toast("User ID not found!", icon='❌')
            return
        st.session_state["user_id"] = user_id
        payload = {
            'user_id': st.session_state["user_id"],
            'name_old': chat_name,
            'name_new': new_name
        }
        response = call_api(f"{api}/mysql/edit_chat", payload=payload, method='put')
        if not response:
            return
        if response.json().get('status') == 200:
            time.sleep(1)
            st.toast('Update chatname success', icon='✅')
            st.session_state['chats'][chat_name]['display_name'] = new_name
            chat_data = st.session_state["chats"].pop(chat_name)
            chat_data["display_name"] = new_name
            st.session_state["chats"][new_name] = chat_data
            st.session_state["current_chat"] = new_name
            switch_chat_name(new_name)
        else:
            message = get_message(response)
            st.toast(message, icon='❌')
    edit_zone = zone.empty()
    time.sleep(0.1)
    with edit_zone.container():
        st.text_input('New Name', st.session_state['chats'][chat_name]['display_name'], key='edited_name')
        column1, _, column2 = st.columns([1, 5, 1])
        column1.button('✅', on_click=edit)
        column2.button('❌')

 def generate_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))

 def render_sidebar_chat_management(zone):
    new_chat_button = zone.button(label="➕ New Chat", use_container_width=True)
    if new_chat_button:
        random_suffix = generate_random_string(13)
        new_chat_name = f"chat_{random_suffix}"
        payload = {'user_id': st.session_state["user_id"], 'chat_name': new_chat_name}
        token = controller.get("token_data")
        headers = {"Authorization": f"Bearer {token}", 'Content-Type': 'application/json', 'accept': 'application/json'}
        url = f"{api}/mysql/chat_history/create"
        response = requests.post(url,json=payload,headers=headers)
        if not sf.check_status_response(response):
           return
        message = get_message(response)
        st.toast(f'{message}', icon='✅')
        st.session_state["current_chat"] = new_chat_name
        new_chat(new_chat_name)
       
    with st.sidebar.container():
        for chat_name in st.session_state["chats"].keys():
            if st.session_state['chats'][chat_name]['is_delete']:
                continue
            if chat_name == st.session_state.get('current_chat'):
                column1, column2, column3 = zone.columns([7, 1, 1])
                column1.button(
                    label='💬 ' + st.session_state['chats'][chat_name]['display_name'],
                    on_click=switch_chat_name,
                    key=chat_name,
                    args=(chat_name,),
                    type='primary',
                    use_container_width=True,
                )
                column2.button(label='📝', key='edit', on_click=edit_chat, args=(chat_name, zone))
                column3.button(label='🗑️', key='remove', on_click=delete_chat, args=(chat_name,))
            else:
                zone.button(
                    label='💬 ' + st.session_state['chats'][chat_name]['display_name'],
                    on_click=switch_chat_name,
                    key=chat_name,
                    args=(chat_name,),
                    use_container_width=True,
                )
    if new_chat_button:
        switch_chat(new_chat_name)
                                



 def render_info_zone(zone, name_user, picture_user, email):
    with zone.container():
        st.markdown(
    f"""
    <style>
        .user_button {{
            display: flex;
            align-items: center;
            cursor: pointer;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }}
        .user_button img {{
            width: 50px;
            height: 50px;
            border-radius: 50%;
            object-fit: cover;
            margin-right: auto;
        }}
        .user_info {{
            display: none;
            margin-top: 10px;
        }}
        .user_name {{
            margin-left: auto;
        }}
    </style>
    <div class="user_button" id="user_button_{name_user}" onclick="showUserInfo('{name_user}')">
        <img src="{picture_user}">
        <span class="user_name">{name_user}</span>
    </div>
    <div class="user_info" id="user_info_{name_user}">
        <p>{email}</p>
        <button onclick="logout()">Confirm Logout</button>
    </div>
    <script>
        function showUserInfo(name) {{
            var userInfo = document.getElementById("user_info_" + name);
            if (userInfo.style.display === "none") {{
                userInfo.style.display = "block";
            }} else {{
                userInfo.style.display = "none";
            }}
        }}
        function logout() {{
            StreamlitApp.reconnect();
        }}
    </script>
    """, unsafe_allow_html=True
)

 import json

 def handle_response(response):
    if response.status_code == 403:
        sf.refresh_token_account()
        token = st.session_state["token"]
        headers["Authorization"] = f"Bearer {token}"
        return requests.request(response.request.method, response.request.url, headers=headers, params=response.request.params, json=response.request.body)
    return response

 def process_request(url, method='GET', headers=None, params=None, json_data=None):
    if method == 'POST':
        response = requests.post(url, headers=headers, params=params, json=json_data)
    else:
        response = requests.get(url, headers=headers, params=params)
    
    response = handle_response(response)
    if not sf.check_status_response(response):
        return None
    return response

 def render_sidebar():
    chat_name_container = st.sidebar.container()
    info_zone = st.sidebar.empty()
    user_id = st.session_state["user_id"]
    try:
        if len(st.session_state["chats"]) == 0:
            st.session_state["generate_question"] = []
            st.session_state["text_all"] = ""
            render_chat_history(st.session_state["user_id"])
            st.toast("Welcome to chatbot. Please wait setup", icon='✅')

            token = st.session_state["token"]
            headers = {
                "Authorization": f"Bearer {token}",
                'Content-Type': 'application/json',
                'accept': 'application/json'
            }
            params = {'user_id': st.session_state["user_id"]}
            url1 = f"{api}/file/chatbot/download_folder"
            res1 = process_request(url1, method='POST', headers=headers, json_data=params)

            if res1:
                status = res1.json()['status']
                if status == 200:
                    api_endpoint = f"{api}/chat/chatbot/extract_file/{user_id}"
                    response = process_request(api_endpoint, headers=headers)

                    if response and response.status_code == 200:
                        text_all = response.json()['data']['text_all']
                        st.session_state["text_all"] = json.dumps(text_all)

                    api_generate_question = f"{api}/chat/chatbot/generate_question/{user_id}"
                    response_generate_question = process_request(api_generate_question, headers=headers)

                    if response_generate_question and response_generate_question.status_code == 200:
                        question = response_generate_question.json()['data']['question']
                        st.session_state["generate_question"] = question
                        st.toast("Generate question success", icon='✅')
                else:
                    message = get_message(res1)
                    st.toast(message, icon='❌')
    except Exception as e:
        st.toast(f"An error occurred: {str(e)}", icon='❌')

    render_sidebar_chat_management(chat_name_container)
    name_user = st.session_state["name_user"]
    render_info_zone(info_zone, name_user, st.session_state['current_photo_url'], controller.get('email'))

 def render_user_message(message, zone):
    if st.session_state.get("theme") == "dark":
        text_color= "#FFFFFF"
        background_color =  "#222222"
    else:
        background_color = "#f1f1f1"
        text_color = "#000000" 
    col1, col2 = zone.columns([8, 1])
    col1.markdown(
        f"<div style='clear: both; float: right; display: inline-block; text-align: left; background-color: {background_color}; color: {text_color}; padding: 10px; margin-bottom: 10px; border-radius: 13px; max-width: 70%; word-wrap: break-word;'>{message}</div>",
        unsafe_allow_html=True
    )
    picture_user = st.session_state['current_photo_url'] 
    col2.markdown(f'<img src="{picture_user}" style="width: 38px; height: 38px; border-radius: 50%;">', unsafe_allow_html=True)

 @st.experimental_dialog("Data relevant", width="large")
 def data_relevant_show(id):
    params = {'chat_detail_id': str(id)}
    api_endpoint = f"{api}/mysql/data_relevant/{id}"
    chat_detail_data = requests.get(api_endpoint)
    if not sf.check_status_response(chat_detail_data):
                  return
    elif chat_detail_data.json()['status'] != 200:
                 message = get_message(chat_detail_data)
                 st.toast(message, icon='❌')
    data = chat_detail_data.json()['data']
    data_relevant = data.get('data_relevant', "")
    source_file = data.get('source_file', "")
    restored_list1 = data_relevant.split("<Data_Relevant>")
    restored_list2 = source_file.split("<Source_File>")
    if len(restored_list1) >= 2:
        for i, (item1, item2) in enumerate(zip(restored_list1, restored_list2)):
            with st.expander(f"{item2}"):
                st.markdown(f"**Reference**: {item1}")
                st.markdown(f"**Source File**: {item2}")
    else:
        st.markdown(f"**Source File**: {source_file}")
        st.markdown(f"**Data Relevant**: {data_relevant}")

 def render_ai_message1(message, data_relevant, source, id, zone):
    col1, col2 = zone.columns([1, 8])
    st.markdown("\n")
    col1.markdown('<img src="https://github.com/vonhuy1/juice-shop/blob/main/445381971_1127721758417646_4619123122720161571_n.png?raw=true" style="width: 38px; height: 38px; border-radius: 50%;">', unsafe_allow_html=True)
    col2.markdown(
        f"<div style='clear: both; display: inline-block; text-align: left; word-wrap: break-word;'>{message}</div>",
        unsafe_allow_html=True
    )
    col2.markdown("<hr>", unsafe_allow_html=True)
    if col2.button('Reference', key=f"btn_chat_detail_{id}"):
           data_relevant_show(id) 

 def render_history_answer(chat, zone):
    zone.empty()
    time.sleep(0.1)
    with zone.container():
        if chat['messages']:
           st.caption(f"""ℹ️ Prompt: {chat["messages"][0]['content']}""")
           html_content = """
    <p>Welcome to PY ChatBot. Feel free to explore the information provided and reach out if you have any questions.</p>"""
           st.markdown(html_content, unsafe_allow_html=True)
           if st.session_state["generate_question"] != False:
            list_question = st.session_state["generate_question"]
            i = 0
            for x in list_question:
               with stylable_container(
           "style123",     
             css_styles="""
          button {     
           background-color: #fff;
           color: #136ec4d9;
           border-radius: 12px;
           justify-content: left;
           height: min-content;
           width: 475px;
           display: inline-block; 
           text-align: left;
           overflow-wrap: break-word;
           
           }""",
        ):
                    button_click =  st.button(" ➤ " + x, use_container_width=True,key="abc"+ f"{i}",help= "Send Ask")
                    if button_click:
                        st.session_state['input'] = x
                        st.session_state["call_handle_ask"] = True
               i = i +1
            st.markdown("\n")
        if chat["question"]:
            for i in range(len(chat["question"])):
                render_user_message(chat["question"][i], st)
                if i < len(chat["answer"]):
                    render_ai_message1(chat["answer"][i], chat["data_relevant"][i], chat["source_file"][i], chat["id"][i], st)
 st.session_state["stop_query"] = False

 def render_last_answer(question, chat, zone):
    answer_zone = zone.empty()   
    chat["messages"].append({"role": "user", "content": question})
    chat["question"].append(question)
    current_chat_key = st.session_state.get('current_chat')
    current_chat_data = st.session_state['chats'].get(current_chat_key)
    chat_name = current_chat_data['display_name']
    st.session_state["current_chat"] = chat_name
    answer = ""
    token = st.session_state["token"]
    with st.spinner("Waiting for response..."):
            token = st.session_state["token"]
            api_endpoint = f"{api}/chat/chatbot/query"
            headers1 = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/x-www-form-urlencoded',
    'accept': 'application/json'}
            data= {'user_id': st.session_state["user_id"],
                   'text_all': st.session_state["text_all"],
                   'question': question,
                   'chat_name': chat_name}
            result = requests.post(api_endpoint, data=data,headers=headers1)
            if result.status_code == 403:
             sf.refresh_token_account()
             token = st.session_state["token"]
             headers = {
         "Authorization": f"Bearer {token}",
         "Content-Type": "application/x-www-form-urlencoded",
    "accept": "application/json"
          }
             result = requests.post(api_endpoint, data = data,headers=headers)
             if not sf.check_status_response(result):
                 return
             if result.status_code == 200:
              status = result1.json()['status']
              data = result.json()['data']
              if status == 500:
               message = get_message(result)
               st.toast(message, icon='❌')
              if status == 404:
               message = get_message(result)
               st.toast(message, icon='❌')
              elif status == 200:
               result1 = data["answer"]
               data_relevant = data["data_relevant"]
               source = data["sources"]
               id = data["id"]
               if not result1: 
                answer = "No Answer"
               else:
                answer += result1
                chat["messages"].append({"role": "assistant", "content": answer})
                chat["answer"].append(answer)
                chat["data_relevant"].append(data_relevant)
                chat["source_file"].append(source)
                chat["id"].append(id)
                render_ai_message1(answer,data_relevant,source,id,answer_zone)
                st.toast("Question success", icon='✅')         
            elif result.status_code == 400:
             message = get_message(result)
             st.toast(message, icon='❌')
            elif result.status_code == 422:
             message = "The parameter passed is not valid. Unprocessable entity"
             st.toast(message, icon='❌')
            elif result.status_code == 502:
              message = "Bad Gateway"
              st.toast(message, icon='❌')
            elif result.json()['status'] != 200:
                 message = get_message(result)
                 st.toast(message, icon='❌')
            elif result.status_code == 200:
              status = result.json()['status']
              data = result.json()['data']
              if status == 500:
               message = get_message(result)
               st.toast(message, icon='❌')
              if status == 404:
               message = get_message(result)
               st.toast(message, icon='❌')
              elif status == 200:
               result1 = data["answer"]
               data_relevant = data["data_relevant"]
               source = data["sources"]
               id = data["id"]
               if not result1: 
                answer = "No Answer"
               else:
                 answer += result1
                 chat["messages"].append({"role": "assistant", "content": answer})
                 chat["answer"].append(answer)
                 chat["data_relevant"].append(data_relevant)
                 chat["source_file"].append(source)
                 chat["id"].append(id)
                 render_ai_message1(answer,data_relevant,source,id,answer_zone)
                 st.toast("Question success", icon='✅')
 def delete_last_chat(token, chat_name):
    url = f"{api}/mysql/chat_history/delete_last_chat_record"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "accept": "application/json"
    }
    payload = {
        "user_id": st.session_state["user_id"],
        "chat_name": chat_name
    }
    requests.delete(url, json=payload, headers=headers)
 
 def render_stop_generate_button(chat,zone):
    def stop():
        token = st.session_state["token"]
        url = f"{api}/mysql/chat_history/delete_last_chat_record"
        headers = {
                       "Authorization": f"Bearer {token}",
                       "Content-Type": "application/json",
                       "accept": "application/json"
                     }
        payload= {
                        "user_id": st.session_state["user_id"],
                        "chat_name": chat["display_name"]}
        requests.delete(url,json=payload,headers=headers)
        chat["question"].pop(-1)
        chat["data_relevant"].pop(-1)
        chat["source_file"].pop(-1)
        chat["id"].pop(-1)
        chat["messages"].pop(-1)
        chat["answer"].pop(-1)
        st.session_state['regenerate'] = False     
    zone.columns((2, 1, 2))[1].button('■', on_click=stop)
   
 def render_regenerate_button(chat, zone):
    def regenerate():
        chat_id = chat["id"][-1]
        token = st.session_state["token"]
        headers = {
         "Authorization": f"Bearer {token}",
         "Content-Type": "application/json",
         "accept": "application/json"
          }
        data = {
            "user_id":  st.session_state["user_id"] ,
            "id_chat_detail": chat_id
        }
        url = f"{api}/mysql/detail_chat/delete"
        requests.delete(url,json=data, headers=headers)
        chat["id"].pop(-1)
        chat["messages"].pop(-1)
        chat["answer"].pop(-1)
        st.session_state['regenerate'] = True
        st.session_state['last_question'] = chat["question"].pop(-1)
    zone.columns((2, 1, 2))[1].button('🔄 Regenerate', type='primary', on_click=regenerate)
 css_voice = """
<style>
.myButton {
    background-color: var(--background-color);
    border: 1px solid #174bb2;
    border-radius: 8px;
    color: var(--text-color);
    cursor: pointer;
    font-family: var(--font);
    font-size: 14px;
    padding: 8px 10px;
    width: 80px !important;
    float: right !important;;
    background-color: #062a21 !important;
}
</style>
"""

 st.markdown(css_voice, unsafe_allow_html=True)
 def render_chat(chat_name):
    css = """
<style>
.st-emotion-cache-7xfda7 {
    display: inline-flex;
    -webkit-box-align: center;
    align-items: center;
    -webkit-box-pack: center;
    justify-content: center;
    font-weight: 400;
    padding: 0.25rem 0.75rem;
    border-radius: 0.5rem;
    min-height: 38.4px;
    margin: 0px;
    line-height: 1.6;
    width: 100%;
    user-select: none;
    background: -webkit-linear-gradient(#ff520b, #fdffd0);
    color: rgb(255, 255, 255);
    border: 1px solid #dc3545;
}
</style>
"""
    st.markdown(css, unsafe_allow_html=True)
    css_1 = """
        <style>
         .st-emotion-cache-1jmvea6 p {
            word-break: break-word;
            margin-bottom: 0px;
            font-size: 16px;
            font-weight: bold;
}
        </style>
    """
    st.markdown(css_1, unsafe_allow_html=True)
    def handle_ask():
        text_str = json.loads(st.session_state["text_all"])
        if not isinstance(text_str, list):
            if text_str in {"No Data"}:
                st.toast("Please load file after send message", icon='❌')
        else:
           if st.session_state['input']:
             re_generate_zone.empty()
             render_user_message(st.session_state['input'], last_question_zone)
             render_stop_generate_button(chat,stop_generate_zone)
             render_last_answer(st.session_state['input'], chat, last_answer_zone)
             st.session_state["call_handle_ask"] = False
             st.rerun()
                                    
    def handle_ask_1(query):
      if query != "":
        conversation_zone1 = st.container()
        stop_generate_zone1 = conversation_zone1.empty()
        render_user_message(query, last_question_zone)
        render_stop_generate_button(chat,stop_generate_zone)
        render_last_answer(query, chat, last_answer_zone)
        if st.session_state.get('regenerate'):
            render_user_message(st.session_state['last_question'], last_question_zone)
            render_stop_generate_button(chat,stop_generate_zone1)
            render_last_answer(st.session_state['last_question'], chat, last_answer_zone)
            st.session_state['regenerate'] = False
        if chat["answer"]:
            stop_generate_zone1.empty()
        query = ""
    if chat_name not in st.session_state["chats"]:
        st.error(f'{chat_name} does not exist')
        return
    chat = st.session_state["chats"][chat_name]
    if chat['is_delete']:
        st.error(f"{chat_name} is deleted")
        st.stop()
    if len(chat['messages']) == 1:
        chat["messages"][0]['content'] = "Hello this is Py Chatbot"

    conversation_zone = st.container()
    history_zone = conversation_zone.empty()
    css_voice = """
<style>
.myButton {
    background-color: var(--background-color);
    border: 1px solid #174bb2;
    border-radius: 8px;
    color: var(--text-color);
    cursor: pointer;
    font-family: var(--font);
    font-size: 14px;
    padding: 8px 10px;
    width: 80px !important;
    float: right !important;;
    background-color: #062a21 !important;
}
</style>
"""
    st.markdown(css_voice, unsafe_allow_html=True)
    text_received = speech_to_text(start_prompt="🎙️", stop_prompt="🛑", language='vi', just_once=True, key='STT345')
    css_voice = """
<style>
.myButton {
    background-color: var(--background-color);
    border: 1px solid #174bb2;
    border-radius: 8px;
    color: var(--text-color);
    cursor: pointer;
    font-family: var(--font);
    font-size: 14px;
    padding: 8px 10px;
    width: 80px !important;
    float: right !important;;
    background-color: #062a21 !important;
}
</style>
"""
    st.markdown(css_voice, unsafe_allow_html=True)
    last_question_zone = conversation_zone.empty()
    last_answer_zone = conversation_zone.empty()
    render_history_answer(chat, history_zone)
    if text_received:
           handle_ask_1(text_received)
    ask_form_zone = st.empty()
    
    ask_form = ask_form_zone.form(chat_name)
    col1, col2 = ask_form.columns([10,1])
    col1.text_area("😃 You: ",
                   key="input",
                   max_chars=4000, height=120,
                   label_visibility='collapsed')
    with col2.container():
        for _ in range(2):
            st.write('\n')
        st.form_submit_button("↑", on_click=handle_ask)
    stop_generate_zone = conversation_zone.empty()
    re_generate_zone = conversation_zone.empty()
    if st.session_state["call_handle_ask"] == True:
         handle_ask()
         st.session_state["call_handle_ask"] = False
         
    if st.session_state.get('regenerate'):
        render_user_message(st.session_state['last_question'], last_question_zone)
        render_stop_generate_button(chat,stop_generate_zone)
        render_last_answer(st.session_state['last_question'], chat, last_answer_zone)
        st.session_state['regenerate'] = False
    if chat["answer"]:
        stop_generate_zone.empty()
        render_regenerate_button(chat, re_generate_zone)
    render_footer()      

 def load_chat_history(chat_name, chat_id):
    user_id = st.session_state["user_id"]
    token = st.session_state["token"]
    params = {'chat_id': chat_id, 'user_id': user_id}
    headers = {"Authorization": f"Bearer {token}", 'accept': 'application/json'}
    api_endpoint = f"{api}/mysql/detail_chat/{user_id}/{chat_id}"
    
    def fetch_chat_history():
        response = requests.get(api_endpoint, headers=headers)
        if response.status_code == 403:
            sf.refresh_token_account()
            token = st.session_state["token"]
            headers["Authorization"] = f"Bearer {token}"
            response = requests.get(api_endpoint, headers=headers)
        return response
    
    chat_detail_data = fetch_chat_history()
    
    if not sf.check_status_response(chat_detail_data):
        return
    
    if chat_detail_data.json()['status'] != 200:
        message = chat_detail_data.json()['data']['message']
        st.toast(f"{message}", icon='❌')
        return
    
    new_chat(chat_name)
    chat = st.session_state["chats"][chat_name]
    chat_detail_data1 = chat_detail_data.json()['data']['detail_chat']
    
    for chat_detail in chat_detail_data1:
        you_ms = chat_detail['question']
        ai_ms = chat_detail['answer']
        data_relevant = chat_detail['data_relevant']
        source = chat_detail["source_file"]
        id = chat_detail["id"]
        chat["question"].append(you_ms)
        chat["answer"].append(ai_ms)
        chat["data_relevant"].append(data_relevant)
        chat["source_file"].append(source)
        chat["id"].append(id)
        chat["messages"].append({"role": "assistant", "content": ai_ms})

 def render_chat_history(user_id, max_retries=5, retry_delay=2):
    params = {'user_id': user_id}
    api_endpoint = f"{api}/mysql/chat_history/{user_id}"
    token = st.session_state["token"]
    headers = {"Authorization": f"Bearer {token}", 'accept': 'application/json'}
    
    retries = 0
    
    while retries < max_retries:
        response = requests.get(api_endpoint,headers=headers)
        if not sf.check_status_response(response):
            return
        elif response.status_code == 403:
            sf.refresh_token_account()
            retries += 1
            time.sleep(retry_delay)
            continue
        elif response.json()['status'] != 200:
            message = response.json()['data']['message']
            st.toast(f"{message}", icon='❌')
            return
        
        response_json = response.json()
        chats_data = response_json['data']['chat']
        
        if chats_data:
            for chat_data in chats_data:
                chat_id = chat_data['id']
                chat_name_1 = chat_data['chat_name']
                load_chat_history(chat_name_1, chat_id)
                chat = st.session_state["chats"][chat_name_1]
                place_holder = st.empty()
                conversation_zone1 = place_holder.container()
                history_zone1 = conversation_zone1.empty()
                st.session_state["current_chat"] = chat_name_1
                history_zone1.empty()
                conversation_zone1.empty()
                place_holder.empty()
            return 
        else:
            st.toast("No chat history available.", icon='ℹ️')
            return
    
    st.toast("Failed to fetch chat history after multiple attempts.", icon='❌')
  
 css_2vdko = """
<style>
.st-emotion-cache-2vdko{
    margin-top: -30px;
}
</style>
"""
 st.markdown(css_2vdko, unsafe_allow_html=True)
    
 css = """
<style>
.st-emotion-cache-7xfda7 {
    display: inline-flex;
    -webkit-box-align: center;
    align-items: center;
    -webkit-box-pack: center;
    justify-content: center;
    font-weight: 400;
    padding: 0.25rem 0.75rem;
    border-radius: 0.5rem;
    min-height: 38.4px;
    margin: 0px;
    line-height: 1.6;
    width: 100%;
    user-select: none;
    background: -webkit-linear-gradient(#ff520b, #fdffd0);
    color: rgb(255, 255, 255);
    border: 1px solid #dc3545;
}
</style>
"""
 st.markdown(css, unsafe_allow_html=True)
 css_font = """
<style>
.st-emotion-cache-j6qv4b p {
 font-family: inherit;
}""" 
 st.markdown(css_font,unsafe_allow_html=True)
 css_1 = """
        <style>
         .st-emotion-cache-1jmvea6 p {
            word-break: break-word;
            margin-bottom: 0px;
            font-size: 16px;
            font-weight: bold;
}
        </style>
    """
 st.markdown(css_1,unsafe_allow_html=True)
 
 init_session()
 render_sidebar()
 if st.session_state.get("current_chat"):
           render_chat(st.session_state["current_chat"])
 if len(st.session_state["chats"]) == 0 :
        name = generate_random_string(13)
        payload = {'user_id': st.session_state["user_id"], 'chat_name': name}
        token = controller.get("token_data")
        headers = {"Authorization": f"Bearer {token}", 'Content-Type': 'application/json', 'accept': 'application/json'}
        url = f"{api}/mysql/chat_history/create"
        response = requests.post(url,json=payload,headers=headers)
        if not sf.check_status_response(response):
            return
        message = get_message(response)
        st.toast(f'{message}', icon='✅')
        switch_chat(new_chat(f"Chat_{name}"))