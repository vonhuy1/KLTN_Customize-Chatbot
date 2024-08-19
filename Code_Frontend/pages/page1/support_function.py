import requests
import streamlit as st
import json, os
from streamlit_cookies_controller import CookieController
import time
import requests
from dotenv import load_dotenv
load_dotenv()
API = os.getenv("BE_API")
api = API
controller = CookieController()
token = controller.get('token_data')
def get_message(result):
   res = result.json()['data']
   message = res["message"]
   return message

def check_status_response(response):
    if response.status_code == 422:
        message = "Unprocessable Entity"
        st.toast(f"{message}", icon='❌')
        return False
    elif response.status_code == 500:
        message = "Internal Server Error"
        st.toast(f"{message}", icon='❌')
        return False
    elif response.status_code == 404:
        message = "Not found"
        st.toast(f"{message}", icon='❌')
        return False
    elif response.status_code == 502:
        message = "Bad Gateway"
        st.toast(f"{message}", icon='❌')
        return False
    elif response.json()['status'] != 200:
        message =  response.json()['data']['message']
        st.toast(f"{message}", icon='❌')
        return False
    return True

def refresh_token_account():
        headers = {
         "Content-Type": "application/json",
         "accept": "application/json"
          }
        token = controller.get("refresh_token")
        api_getfile1 = f"{api}/auth/refresh_token"
        payload = {
        'refresh_token': token,
        }
        response = requests.post(api_getfile1,json=payload,headers=headers)
        if not check_status_response(response):
                  return
        status = response.json()['status']
        result = response.json()['data']
        if status == 200:
          st.session_state["token"] = result["token_new"]
          controller.set('token_data', result["token_new"])
          controller.set('session_id', result["session_id"])
          st.session_state["session_id"] = result["session_id"]
        if status == 415:
            message = get_message(response)
            st.toast(message, icon='❌')
        if status == 404:
            message = get_message(response)
            st.toast(message, icon='❌')
        if status == 400:
          message = get_message(response)
          st.toast(message, icon='❌')
        if status == 500:
          st.toast("Login again",icon = '❌')
          controller.set('token_data', None,secure=True,same_site='strict')
          controller.set('session_id',None,secure=True,same_site='strict')
          time.sleep(1.5)
          st.markdown('<meta http-equiv="refresh" content="0;URL=http://localhost:8501/login"/>', unsafe_allow_html=True)
import streamlit as st
import jwt
import datetime
import requests
def decode_token(token):
    decoded = jwt.decode(token, options={"verify_signature": False})
    return decoded.get('exp')

def check_time_token(token):
    exp_timestamp = decode_token(token)
    exp_time = datetime.datetime.fromtimestamp(exp_timestamp)
    remaining_time = exp_time - datetime.datetime.now()
    if remaining_time < datetime.timedelta(minutes=20):
        refresh_token_account()