import streamlit as st
import streamlit as st
from dotenv import load_dotenv
import os
load_dotenv()
API = os.getenv("BE_API")
from pages.page1 import support_function as sf


def show_about():
    from streamlit_extras.stylable_container import stylable_container
    api = API
    from streamlit_cookies_controller import CookieController
    controller = CookieController()
    token = controller.get('token_data')
    
    import requests,time
    import datetime
    st.session_state["uid"] = ""
    st.session_state['current_photo_url'] = ""
    st.session_state['name_user'] = ""
    st.session_state['email'] = ""
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
    
    
    st.header("Community", divider='orange')
    st.write(
        """
        Welcome to our community of ChatBot PY users! This is the place where you can connect with other users, share your experiences, and learn more about how to make the most of our application. Whether you're a beginner or an expert, you'll find valuable insights and support here.

        Join our Facebook group to stay updated on the latest news, participate in discussions, and get help from fellow community members. We encourage you to ask questions, share your feedback, and collaborate with others.

        [Join our ChatBot PY Community](https://www.facebook.com/groups/1508998179652455)

        Together, we can make ChatBot PY even better!
        """
    )
    st.header("GitHub", divider='orange')
    st.write("GitHub: https://github.com/gabrieltempass/streamlit-navigation-bar")
