import streamlit as st
from dotenv import load_dotenv
import os
load_dotenv()
API = os.getenv("BE_API")
from pages.page1 import support_function as sf

def show_profile():
 from streamlit_extras.stylable_container import stylable_container
 api = API
 from streamlit_cookies_controller import CookieController
 controller = CookieController()
 import requests,time
 token = controller.get('token_data')
 check_google = controller.get('login_google')
 st.session_state["uid"] = ""
 st.session_state['current_photo_url'] = ""
 st.session_state['name_user'] = ""
 st.session_state['email'] = ""
 import datetime 
 def get_message(result):
   res = result.json()['data']
   message = res["message"]
   return message
 
 
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
                user_info_data = requests.get(url_info, headers=headers)
                if not sf.check_status_response(user_info_data):
                       return
                if user_info_data.status_code == 403:
                    sf.refresh_token_account()
                    token = controller.get("token_data")
                    headers = {"Authorization": f"Bearer {token}",'Content-Type': 'application/json', 'accept': 'application/json'}
                    url_info = f"{api}/default/info_user/{user_id}"
                    user_info_data = requests.get(url_info, headers=headers)
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
                
 def check_state_login():
    user_id = st.session_state.get("user_id")
    api_url = f"{api}/users/check_state_login"
    params = {
    'user_id': user_id,
    'session_id_now': controller.get('session_id')
}   
    response = requests.get(api_url, params=params)
    if not sf.check_status_response(response):
                  return
    status = response.json()['status']
    if status == 200:
      check_result = response.json()['data']['check']
      if check_result == False:
                st.toast("Your account was accessed from a different location.",icon="❌")
                controller.set('token_data', None )
                controller.set('session_id',None)
                controller.set('email',None)
                time.sleep(2)
                st.markdown('<meta http-equiv="refresh" content="0;URL=http://localhost:8501/login" />', unsafe_allow_html=True)
    else:
         message = response.json()['data']['message']
         st.toast(f"{message}", icon='❌')
 if check_google == True:
    page = st.sidebar.radio("Select the function in profile", ["User Information","Logout"])
 elif check_google == False or check_google is None: 
    page = st.sidebar.radio("Select the function in profile", ["User Information", "Change Password","Logout"])
 
 if page == "User Information":
    st.header("User Information",divider="green")

    css1 = """
<style>
.stTextInput label {
    font-weight: 600;
    color: #4050b0;
    font-weight: bold;
    font-size: 20px;
    /**/
}
</style>
"""

    st.markdown(css1, unsafe_allow_html=True)
    css = """
<style>
.st-emotion-cache-1jmvea6 p {
    word-break: break-word;
    margin-bottom: 0px;
    font-size: 18px;
    border: 2px;
    font-weight: bold;
    color: black;
}
</style>
"""
    st.markdown(css, unsafe_allow_html=True)
    user_id = st.session_state["uid"]
    current_username =  st.session_state["name_user"]
    current_photo_url = st.session_state['current_photo_url'] 
    if current_photo_url  == "N/A" :
        current_photo_url ="https://inkythuatso.com/uploads/images/2021/12/logo-hcmute-inkythuatso-17-13-52-06.jpg"
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
    css1 = """
<style>
.st-eu {
    justify-content: center;
    background: white !important;
    background-clip: text;
    color: transparent;
    font-weight: bold !important;
}
}
</style>
"""
    st.markdown(css1,unsafe_allow_html=True)
    css1 = """
<style>
.st-bb {
    justify-content: center;
    color: #4050b0;
    font-weight:bold !important;
}
</style>
"""
    st.markdown(css1, unsafe_allow_html=True)
    css1 = """
<style>
.st-ht {
    justify-content: center;
    color: #000;
    font-weight:bold !important;
}
</style>
"""
    st.markdown(css1, unsafe_allow_html=True)
    st.text_input(":blue[User Id]", value=user_id, key="user_id_input", disabled=True)
    st.text_input(":blue[Email]", value=st.session_state["email"] , key="user_id_input1", disabled=True)
    username = st.text_input(":blue[User Name]", value=current_username, key="username_input")
    uploaded_file = st.file_uploader(":blue[Upload Image]", type=["png", "jpg", "jpeg"], key="new_image")
    if uploaded_file is not None:
     email = st.session_state["email"]
     temp_image_path = f"temp_image_{email}.png"
    
     with open(f"./image_user/temp_image_{email}.png", "wb") as f:
        f.write(uploaded_file.getbuffer())
     
     api_url = f"{api}/default/upload_image"
     headers = {
        "Authorization": f"Bearer {st.session_state['token']}"
    }
     files = {'file': open(f"./image_user/temp_image_{email}.png", 'rb')}
     data = {'user_id':  st.session_state["user_id"]}
     response = requests.post(api_url, headers=headers, files=files, data=data)
     if not sf.check_status_response(response):
                  return
     elif response.status_code == 403:
         sf.refresh_token_account()
         response = requests.post(api_url, headers=headers, files=files, data=data)
         photo_url_api = response.json()['data']['url']
         current_photo_url = photo_url_api
         st.markdown(f'<img id="current_image" src="{current_photo_url}" style="width: 250px; height: 250px; object-fit: cover; border-radius: 50%; display: block; margin: 0 auto;">', unsafe_allow_html=True)
     elif response.status_code == 200:  
        if response.json()["status"] == 200:
         photo_url_api = response.json()['data']['url']
         current_photo_url = photo_url_api
         st.markdown(f'<img id="current_image" src="{current_photo_url}" style="width: 250px; height: 250px; object-fit: cover; border-radius: 50%; display: block; margin: 0 auto;">', unsafe_allow_html=True)
        else:
            message = response.json()['data']['message']
            st.toast(f"{message}", icon='❌')
            
    else:
     if 'current_photo_url' not in st.session_state:
        st.markdown(f'<img id="current_image" src="{current_photo_url}" style="width: 250px; height: 250px; object-fit: cover; border-radius: 50%; display: none;">', unsafe_allow_html=True)
     else:
        current_photo_url = st.session_state['current_photo_url']
        st.markdown(f'<img id="current_image" src="{current_photo_url}" style="width: 250px; height: 250px; object-fit: cover; border-radius: 50%; display: block; margin: 0 auto;">', unsafe_allow_html=True)
        photo_url_api = current_photo_url
    st.markdown(
    """
    <style>
    .stButton > button {
        margin: 0 auto;
        display: block;
    }
    </style>
    """,
    unsafe_allow_html=True
)
    with stylable_container(
           "black111_save",
         css_styles="""
          button {
           background: -webkit-linear-gradient(#ff688b, #f8e4d9);
           color: black;
           width: 300px;
           border-radius: 9px;
           display:flex;
           align-items: center;
           justify-content: center;
           margin-top: 35px;
           }""",
        ):
                   btnSave= st.button("Save",key = "btnsave123")
    if btnSave:
         with st.spinner("Waiting for update..."):
            user_info = {
                        "user_id": st.session_state["user_id"],
                        "uid": user_id,
                        "email": st.session_state["email"],
                        "display_name": username,
                        "photo_url": photo_url_api
                                  } 
            token = st.session_state["token"]
            headers = {"Authorization": f"Bearer {token}", 'accept': 'application/json'}
            url_update = f"{api}/users/update_user_info"
            response = requests.put(url_update, json=user_info,headers=headers)
            if not sf.check_status_response(response):
                  return
            elif response.status_code == 403:
                sf.refresh_token_account()
                response = requests.put(url_update, json=user_info,headers=headers)
                status = response.json()['status']
                if status == 200:
                  message = get_message(response)
                  st.toast(message, icon='✅')
                  time.sleep(0.5)
                  os.remove(temp_image_path)
                  st.rerun()
                else:
                 if status == 400:
                    message = get_message(response)
                    st.toast(message, icon='❌')
                 if status == 404:
                    message = get_message(response)
                    st.toast(message, icon='❌')
                 if status == 500: 
                    message = get_message(response)
                    st.toast(message, icon='❌')
                 if response.status_code == 502:
                   message = "Bad Gateway"
                   st.toast(message, icon='❌')
                 st.toast("Error", icon='❌')        
            status = response.json()['status']
            if status == 200:
                message = get_message(response)
                st.toast(message, icon='✅')
                time.sleep(0.5)
                st.rerun()
            else:
                if status == 404:
                    message = get_message(response)
                    st.toast(message, icon='❌')
                if status == 400:
                    message = get_message(response)
                    st.toast(message, icon='❌')
                if status == 500: 
                    message = get_message(response)
                    st.toast(message, icon='❌')
                if response.status_code == 502:
                   message = "Bad Gateway"
                   st.toast(message, icon='❌')
                st.toast("Error", icon='❌')    
 elif page =="Change Password":
        st.header("Change Password",divider="orange")
        st.markdown(
    """
    <style>
    .stButton > button {
        margin: 0 auto;
        display: block;
    }
    </style>
    """,
    unsafe_allow_html=True
)       
        css1 = """
<style>
.st-eu {
    justify-content: center;
    color: #098e22;
    font-weight: bold !important;
}
</style>
"""             
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
        css_bb = """
<style>
.st-bb {
    justify-content: center;
    color: #098e22;
    font-weight: bold !important;
}
</style>
"""             
        st.markdown(css_bb,unsafe_allow_html=True)
        st.markdown(css1,unsafe_allow_html=True)
        st.markdown(css_12, unsafe_allow_html=True)
                
        current_password = st.text_input(":green[Current Password]", type ="password", key="current_password", placeholder="Enter Your Current Password")
        password1_sign = st.text_input(":green[New Password]", type="password", key="signup_password1_input", placeholder="Enter Your New Password")
        password2_sign = st.text_input(':green[Confirm New Password]', type="password", key="signup_password2_input", placeholder="Confirm New Password")
        with stylable_container(
           "green",
         css_styles="""
          button {
           background: -webkit-linear-gradient(#04aa7a, #b2d2b2);
           color: white;
           width: 300px;
           border-radius: 6px;
           margin-top: 35px;
           }""",
        ):     btnChangePassword = st.button("Update",key = "updatebtn")
        if btnChangePassword:
                  if current_password is None or current_password== "":
                      st.toast("Current Password is Empty", icon='⚠️')
                  elif password1_sign is None or password1_sign == "":
                     st.toast("New Password is Empty", icon='⚠️')
                  elif password2_sign is None or password2_sign == "":
                      st.toast("Confirm New Password is Empty", icon='⚠️')
                  else:
                      if password1_sign == password2_sign:
                       if current_password != password2_sign:
                        email =  st.session_state["email"]
                        token = st.session_state["token"]
                        headers = {"Authorization": f"Bearer {token}",'Content-Type': 'application/json', 'accept': 'application/json'}
                        payload = {'user_id': st.session_state["user_id"], 'new_password': password1_sign,'current_password':current_password,'confirm_new_password':password2_sign}
                        api_endpoint = f"{api}/users/change_password"
                        result = requests.put(api_endpoint,json=payload,headers=headers)
                        if not sf.check_status_response(result):
                                      return
                        elif result.status_code == 403:
                            sf.refresh_token_account()
                            result = requests.put(api_endpoint,json=payload,headers=headers)
                            status = result.json()['status']
                            if status == 200:
                              message = get_message(result) 
                              time.sleep(3) 
                              st.toast(message, icon='✅') 
                              time.sleep(3)
                              current_password = ""
                              password1_sign = ""
                              password2_sign = ""
                              st.rerun()
                            if status == 400:
                              message = get_message(result)
                              st.toast(message, icon='❌') 
                            if status == 500:
                             message = get_message(result)
                             st.toast(message, icon='❌')
                        status = result.json()['status']
                        if status == 200:
                            message = get_message(result)
                            time.sleep(3)
                            st.toast(message, icon='✅')
                            time.sleep(3)
                            current_password = ""
                            password1_sign = ""
                            password2_sign = ""
                            st.rerun()
                        if status == 400:
                            message = get_message(result)
                            st.toast(message, icon='❌')
                        if status == 404:
                            message = get_message(result)
                            st.toast(message, icon='❌')
                        if status == 500:
                             message = get_message(result)
                             st.toast(message, icon='❌') 
                        if result.status_code == 502:
                            message = "Bad Gateway"
                            st.toast(message, icon='❌')
                        if result.status_code == 422:
                            message = "The parameter passed is not valid. Unprocessable entity"
                            st.toast(message, icon='❌')    
                       else:
                           st.toast("The new password must not be the same as the current password", icon='⚠️')
                      else:
                        st.toast("Passwords Do Not Match", icon='⚠️')
    
 elif page == "Logout":
        controller.set('token_data', None,secure=True,same_site='strict')
        controller.set('session_id',None,secure=True,same_site='strict')
        st.toast("Log out success", icon='✅')
        time.sleep(1.5)
        st.markdown('<meta http-equiv="refresh" content="0;URL=http://localhost:8501/login" />', unsafe_allow_html=True)