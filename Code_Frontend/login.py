import json
from streamlit.components.v1 import html
import requests
import time
from pathlib import Path
from streamlit_oauth import OAuth2Component
from httpx_oauth.clients.google import GoogleOAuth2
import base64
import streamlit as st
from urllib.parse import quote_plus
from streamlit_js_eval import streamlit_js_eval
from streamlit_extras.stylable_container import stylable_container
import re
from streamlit_cookies_controller import CookieController
from dotenv import load_dotenv
import os
load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
EMAIL= os.getenv('EMAIL')
PASSWORD=os.getenv('PASSWORD')
from streamlit.source_util import (
    page_icon_and_name,
    calc_md5,
    get_pages,
    _on_pages_changed
)

is_logged_in = False
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
controller = CookieController()
api = os.getenv('BE_API')
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject, body, to_email):
    from_email = EMAIL
    from_password = PASSWORD
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, from_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

def send_verification_email(to_email, otp_code):
    html_body = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }}

            .container {{
                background-color: #ffffff;
                margin: 0px auto;
                padding: 10px;
                border-radius: 12px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                width: 70%;
                max-width: 500px;
                background-image: url('https://www.transparenttextures.com/patterns/white-diamond.png');
                background-size: cover;
            }}
            .header {{
                text-align: center;
                padding: 20px 0;
                background-color: #cfd86df7;
                color: black;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
            }}
            .header img {{
                width: 100px;
                height: 100px;
            }}
            .header h2 {{
                margin: 10px 0;
                color: white;
            }}
            .content {{
                padding: 20px;
                text-align: center;
                background-color: #7d862166;
                font-family: fangsong;
                font-size: 14px;
                font-weight: bolder;
            }}
            .otp-code {{
                font-size: 26px;
                font-weight: bold;
                color: #4CAF50;
                background-color: #ffffff;
                padding: 10px;
                border-radius: 6px;
                display: inline-block;
                margin-top: 10px;
                border: 2px solid #4CAF50;
            }}
            .footer {{
                text-align: center;
                padding: 18px 0;
                border-top: 1px solid #eeeeee;
                color: #ba2020;
                font-size: 13px;
                font-weight: bold;
            }}
            .footer a {{
                color: rgb(26, 115, 232);
                text-decoration: none;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <img src="https://github.com/vonhuy1/juice-shop/blob/main/445381971_1127721758417646_4619123122720161571_n.png?raw=true" style="width: 130px; height: 130px; border-radius: 50%;" alt="Logo">
                <h2>Verify Email MyChatBot</h2>
            </div>
            <div class="content">
                <p>Hello, {to_email}</p>
                <p>This is code verfiy:</p>
                <p class="otp-code">{otp_code}</p>
                <p>Best regards,<br>Vo Nhu Y</p>
            </div>
            <div class="footer">
                <p>If you did not request this, please ignore this email.</p>
                <p>Contact us at <a href="mailto:20133118@student.hcmute.edu.vn">20133118@student.hcmute.edu.vn</a></p>
            </div>
        </div>
    </body>
    </html>
    """

    send_email(
        subject="Verify Email SignUp",
        body=html_body,
        to_email=to_email
    )
    

def load_multi_pages():
    pages = get_pages(__file__)
    main_script_path = Path(__file__)
    pages_dir = main_script_path.parent / "pages"
    script_paths = [f for f in pages_dir.glob("*.py") if f.name != '__init__.py']
    for path in script_paths:
        script_path_str = str(path.resolve())
        pi, pn = page_icon_and_name(path)
        psh = calc_md5(script_path_str)
        pages[psh] = {
            "page_script_hash": psh,
            "page_name": pn,
            "icon": pi,
            "script_path": script_path_str,
        }
        _on_pages_changed.send()

def nav_page(page_name, timeout_secs=3):
    nav_script = """
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {
                    if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
                        links[i].click();
                        return;
                    }
                }
                var elasped = new Date() - start_time;
                if (elasped < timeout_secs * 1000) {
                    setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
                } else {
                    alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
                }
            }
            window.addEventListener("load", function() {
                attempt_nav_page("%s", new Date(), %d);
            });
        </script>
    """ % (page_name, timeout_secs)
    html(nav_script)

def hide_multi_pages():
    current_pages = get_pages(__file__)
    page_keys = [key for key, value in current_pages.items() if value['page_name'] != 'login' and value['page_name'] != 'main' and value['page_name'] != 'forgot']
    for key in page_keys:
        del current_pages[key]

def save_global_var_to_url(global_var):
    encoded_global_var = quote_plus(str(global_var))
    st.experimental_set_query_params(global_var=encoded_global_var)
    st.markdown('[Go to Chatbot](http://localhost:8501)', unsafe_allow_html=True)

def render_welcome():
        time.sleep(3)
        st.toast("Ridirect to page Home", icon='✅')
        nav_page('main')

def check_email(email):
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

def main():
    global is_logged_in
    css = """
<style>

 @keyframes colorChange {
  0% { color: #FF5733; }  /* Red */
  10% { color: #FF8D1A; } /* Orange */
  20% { color: #FFC300; } /* Yellow */
  30% { color: #DAF7A6; } /* Light Green */
  40% { color: #33FF57; } /* Green */
  50% { color: #33FFBD; } /* Teal */
  60% { color: #33C3FF; } /* Light Blue */
  70% { color: #3380FF; } /* Blue */
  80% { color: #8D33FF; } /* Purple */
  90% { color: #FF33C4; } /* Pink */
  100% { color: #FF5733; } /* Red */
}

.marquee {
  font-family: "Source Sans Pro", sans-serif;
  font-weight: 700;
  padding: 1.25rem 0px 1rem;
  margin: 0px;
  line-height: 1.2;
  font-size: 35px;
  animation: colorChange 1.5s infinite;
  overflow: hidden;
  white-space: nowrap;
  display: inline-block;
  width: 100%;
}

.marquee span {
  display: inline-block;
  animation: marquee 12s linear infinite;
}

@keyframes marquee {
  from {
    transform: translateX(100%);
  }
  to {
    transform: translateX(-100%);
  }
}
</style>
"""

# HTML code for the marquee element with the title
    marquee_html = """
<div class="marquee">
  <span>💥💥Welcome to my ChatBot💥💥</span>
</div>
"""

# Display the CSS and HTML in Streamlit
    st.markdown(css, unsafe_allow_html=True)
    st.markdown(marquee_html, unsafe_allow_html=True)
    if is_logged_in:
        st.write("User is logged in.")
    else:
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
        if "form_submitted" not in st.session_state:
             st.session_state["form_submitted"] = False

        @st.experimental_dialog("Verify Email")
        def verify_email():
                st.title("Please check your email and enter the OTP we have sent. The OTP is valid for 15 minutes.")
                otp = st.text_input(":black[OTP]", key="user_otp", placeholder="Enter Your OTP")
                with stylable_container(
           "btnVerify",
         css_styles="""
          button {
           background: -webkit-linear-gradient(#1eb6ef, #e6f4e8);
           color: black;
           width: 220px;
           border-radius: 6px;
           font-size: 18px;
           text-shadow: none;
           height: 36px;
           font-family: SFProDisplay-Bold, Helvetica, Arial, sans-serif !important;
           font-weight: bold;

           }""",
        ):     btnVerify = st.button("Verify")
                if btnVerify: 
                    if otp is None or otp == "":
                        st.toast("OTP is Empty", icon='⚠️')
                    email_sign = st.session_state["email_sign"]
                    password_sign = st.session_state["password_sign"]
                    confirm_password_sign = st.session_state["confirm_password_sign"]
                    username_sign = st.session_state["username_sign"]
                    headers = {'Content-Type': 'application/json', 'accept': 'application/json'}
                    payload2 = {'email': email_sign,'otp': otp}
                    api_endpoint2 = f"{api}/otp/verify_otp"
                    res = requests.post(api_endpoint2,json=payload2,headers=headers)
                    if res.status_code == 422:
                            message = "Unprocessable Entity"
                            st.toast(f"{message}", icon='❌')
                    elif res.status_code == 500:
                            message = "Internal Server Error"
                            st.toast(f"{message}", icon='❌')
                    elif res.status_code == 404:
                            message = "Not found"
                            st.toast(f"{message}", icon='❌')
                    elif res.status_code == 200:
                     status_verify = res.json()['status']
                     data_verify = res.json()['data']
                     if status_verify == 200:
                        message = "Verify Successful!"
                        st.toast(message, icon='✅')
                        headers = {'Content-Type': 'application/json', 'accept': 'application/json'}
                        payload = {'email': email_sign, 'password': password_sign,'username':username_sign,"confirm_password":confirm_password_sign}
                        api_endpoint = f"{api}/auth/sign_up"
                        result = requests.post(api_endpoint,json=payload,headers=headers)
                        if result.status_code == 422:
                            message = "Unprocessable Entity"
                            st.toast(f"{message}", icon='❌')
                        elif result.status_code == 500:
                            message = "Internal Server Error"
                            st.toast(f"{message}", icon='❌')
                        elif result.status_code == 404:
                            message = "Not found"
                            st.toast(f"{message}", icon='❌')
                        status = int(result.json()['status'])
                        data = result.json()['data']
                        if status == 200:
                            st.session_state["form_submitted"] = False
                            message = "Sign up Successful!"
                            st.toast(message, icon='✅')
                            time.sleep(1)
                            st.rerun()               
                        else:
                            message = data['message']
                            st.toast(message, icon='❌')
                     else:
                        message = data_verify['message']
                        st.toast(message, icon='❌')
    
        @st.experimental_dialog("Sign up")
        def signup():
                st.session_state["email_sign"] = ""
                st.session_state["password_sign"] = ""
                st.session_state["confirm_password_sign"] = ""
                st.session_state["username_sign"] = ""
                username = st.text_input(":black[Username]", key="username_input", placeholder="Enter Your Username")
                email_sign = st.text_input(":black[Email]", key="signup_email_input", placeholder="abcd@gmail.com")
                password1_sign = st.text_input(":black[Password]", type="password", key="signup_password1_input", placeholder="Enter Your Password")
                password2_sign = st.text_input(':black[Confirm Password]', type="password", key="signup_password2_input", placeholder="Confirm Password")
                with stylable_container(
           "btnSignUP",
         css_styles="""
          button {
           background: -webkit-linear-gradient(#1eb6ef, #e6f4e8);
           color: black;
           width: 220px;
           border-radius: 6px;
           font-size: 18px;
           text-shadow: none;
           height: 36px;
           font-family: SFProDisplay-Bold, Helvetica, Arial, sans-serif !important;
           font-weight: bold;

           }""",
        ):     btnSignUp = st.button("Sign up")
                if btnSignUp:
                  if email_sign is None or email_sign == "":
                      st.toast("Email is Empty", icon='⚠️')
                  elif password1_sign is None or password1_sign == "":
                     st.toast("Password is Empty", icon='⚠️')
                  elif password2_sign is None or password2_sign == "":
                      st.toast("Confirm Password is Empty", icon='⚠️')
                  elif check_email(email_sign) == False:
                      st.toast("Email invalid", icon='⚠️')
                  else: 
                      if password1_sign == password2_sign:
                       headers = {'Content-Type': 'application/json', 'accept': 'application/json'}
                       payload = {'email': email_sign}
                       api_endpoint = f"{api}/users/check_info_google_signup"
                       res = requests.get(api_endpoint,params=payload,headers=headers)
                       if res.status_code == 422:
                            message = "Unprocessable Entity"
                            st.toast(f"{message}", icon='❌')
                       elif res.status_code == 500:
                            message = "Internal Server Error"
                            st.toast(f"{message}", icon='❌')
                       elif res.status_code == 404:
                            message = "Not found"
                            st.toast(f"{message}", icon='❌')
                       if res.json()['status'] != 200:
                            message = res.json()['data']['message']
                            st.toast(f"{message}", icon='❌')
                       check = res.json()['data']['check']
                       if check == True:
                           st.toast("Email Exits", icon='⚠️')
                       if check == False:
                        headers = {'Content-Type': 'application/json', 'accept': 'application/json'}
                        payload1 = {'email': email_sign}
                        api_endpoint1 = f"{api}/otp/create_otp"
                        res = requests.post(api_endpoint1,json=payload1,headers=headers)
                        if res.status_code == 422:
                            message = "Unprocessable Entity"
                            st.toast(f"{message}", icon='❌')
                        elif res.status_code == 500:
                            message = "Internal Server Error"
                            st.toast(f"{message}", icon='❌')
                        elif res.status_code == 404:
                            message = "Not found"
                            st.toast(f"{message}", icon='❌')
                        elif res.json()['status'] != 200:
                           message = res.json()['data']['message']
                           st.toast(f"{message}", icon='❌')
                        elif res.status_code == 200 and res.json()['status'] == 200:
                         otp = res.json()['otp']
                         send_verification_email(email_sign,otp)
                         st.session_state["form_submitted"] = True
                         st.session_state["email_sign"] = email_sign
                         st.session_state["password_sign"] = password1_sign
                         st.session_state["username_sign"] = username
                         st.session_state["confirm_password_sign"] = password2_sign
                         st.rerun()
                      else:
                        st.toast("Passwords Do Not Match", icon='⚠️')
        css111 = """
      <style>
h3 {
    font-family: "Source Sans Pro", sans-serif;
    font-weight: 600;
    letter-spacing: -0.005em;
    display: flex;
    padding: 0.5rem 0px 1rem;
    margin: 0px;
    line-height: 1.2;
    justify-content: center;
    boder: 2px;
    font-weight: bold;
    font-size: 32px;
    background: linear-gradient(to left, #23d6df 30%, #330867 100%);
    background-clip: text;
    color: transparent;
    
}
</style>
"""
        st.markdown(css111, unsafe_allow_html=True)
                  
        with st.form(key='signin'):
                css = """
      <style>
h3 {
    font-family: "Source Sans Pro", sans-serif;
    font-weight: 600;
    letter-spacing: -0.005em;
    display: flex;
    padding: 0.5rem 0px 1rem;
    margin: 0px;
    line-height: 1.2;
    justify-content: center;
    boder: 2px;
    font-weight: bold;
    font-size: 32px;
    background: linear-gradient(to left, #23d6df 30%, #330867 100%);
    background-clip: text;
    color: transparent;
    
}
</style>
"""
                st.markdown(css, unsafe_allow_html=True)
                st.subheader('Login')
                css1 = """
<style>
.stTextInput label {
    font-weight: 600;
    color: #4050b0;
    font-weight: bold;
    font-size: 20px;
    /* Thêm các thuộc tính CSS khác mà bạn muốn */
}
</style>
"""

# Sử dụng element.style để nhúng CSS vào phần tử
                st.markdown(css1, unsafe_allow_html=True)
                css2 = """
<style>
.st-emotion-cache-10trblm {
    position: relative;
    flex: 1 1 0%;
    margin-left: calc(3rem);
    display: flex;
    justify-content: center;
    background: linear-gradient(to left, #23d6df 30%, #330867 100%);
    background-clip: text;
}
</style>
"""
                st.markdown(css2, unsafe_allow_html=True)
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
                email = st.text_input(':blue[Email]', key="email_input",placeholder="abcd@gmail.com")
                password = st.text_input(':blue[Password]', type="password", key="password_input",placeholder="Enter your password ")
                st.markdown(
    '''
    <a href="http://localhost:8501/forgot" style="color: red; text-decoration: underline;float:right;">
        Forgotten password?
    </a>
    ''', 
    unsafe_allow_html=True
)
                with stylable_container(
           "black",
         css_styles="""
          button {
           background: -webkit-linear-gradient(#1eb6ef, #e6f4e8);
           color: black;
           width: 180px;
           border-radius: 9px;
           }""",
        ):
                   button1 = st.form_submit_button("Login")
                
                if button1:
                   if email is  None or email == "":
                            st.toast("Email empty", icon='⚠️')
                   elif password is None or password == "": 
                          st.toast("Password empty", icon='⚠️')
                   elif check_email(email) == True:                         
                        headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}
                        payload = {'email': email, 'password': password}
                        api_endpoint = f"{api}/auth/login"
                        result = requests.post(api_endpoint,json=payload,headers=headers)
                        status = int(result.json()['status'])
                        data = result.json()['data']
                        if status == 500:
                            message = data['message']
                            st.toast(f"{message}", icon='❌')
                            st.session_state["authenticated"] = False
                        elif status == 400:
                            message = data['message']
                            st.toast(message, icon='❌')
                        elif result.status_code == 422:
                            message = "Unprocessable Entity"
                            st.toast(f"{message}", icon='❌')
                        elif result.status_code == 500:
                            message = "Internal Server error"
                            st.toast(f"{message}", icon='❌')
                        elif result.status_code == 502:
                            message = "Bad Gateway"
                            st.toast(f"{message}", icon='❌')
                        elif status == 404:
                            message = data['message']
                            st.toast(f"{message}", icon='❌')
                        elif status == 200:
                            st.session_state["authenticated"] = True
                            token = data['access_token']
                            rf_token= data['refresh_token']
                            
                            session_id = data['session_id']  
                            url_isme = f"{api}/default/is_me"
                            user_data_isme = requests.get(url_isme,params={'token': token})
                            user_id = user_data_isme.json()['data']['user_id']
                            headers = {"Authorization": f"Bearer {token}",'Content-Type': 'application/json', 'accept': 'application/json'}
                            url_info = f"{api}/default/info_user/{user_id}"
                            user_info_data = requests.get(url_info,headers=headers)
                            if user_info_data.status_code == 422:
                              message = "Unprocessable Entity"
                              st.toast(f"{message}", icon='❌')
                            elif user_info_data.status_code == 500:
                              message = "Internal Server Error"
                              st.toast(f"{message}", icon='❌')
                            elif user_info_data.status_code == 404:
                               message = "Not found"
                               st.toast(f"{message}", icon='❌')
                            elif user_info_data.status_code == 200:
                                if user_info_data.json()['status'] != 200:
                                      message = user_info_data.json()['data']['message']
                                      st.toast(f"{message}", icon='❌')
                                data_user = user_info_data.json()['data']
                                user_status = user_info_data.json()['status']
                                uid = data_user["uid"]
                                email = data_user["email"]
                                display_name = data_user["display_name"]
                                st.session_state["user_name"] = display_name    
                                photo_url = data_user["photo_url"]
                                user_info = {
                                "user_id": user_id,
                                "uid": uid,
                                "email": email,
                                "display_name": display_name,
                                "photo_url": photo_url
                                  }
                            headers = {"Authorization": f"Bearer {token}", 'accept': 'application/json','Content-Type': 'application/json'}
                            url_update = f"{api}/users/update_user_info"
                            response = requests.put(url_update, json=user_info,headers=headers)
                            if response.json()['status'] == 200:
                             controller.set('token_data',token,secure= True,same_site='strict')
                             controller.set('refresh_token',token,secure= True,same_site='strict')
                             controller.set('session_id',session_id,secure= True,same_site='strict')
                             controller.set('email',email,secure= True,same_site='strict')
                            elif response.json()['status'] != 200:
                                message = response.json()['data']['message']
                                st.toast(f"{message}", icon='❌')
                            st.toast("Login success", icon='✅')
                   else:
                       st.toast("Email invalid", icon='⚠️')
        if st.session_state["form_submitted"] == True:
            verify_email()     
        with stylable_container(
           "green",
         css_styles="""
          button {
           background: -webkit-linear-gradient(#1ba951, #cad7ae);
           color: black;
           width: 220px;
           border-radius: 9px;
           }""",
        ):
          button1_clicked = st.button("Create new account", key="btnsignup")          
        if button1_clicked:
            signup()
        client = GoogleOAuth2(CLIENT_ID, CLIENT_SECRET)
        AUTHORIZE_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
        TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
        REVOKE_ENDPOINT = "https://oauth2.googleapis.com/revoke"

        if "auth" not in st.session_state:
         try:
          oauth2 = OAuth2Component(client=client,client_id=CLIENT_ID,client_secret= CLIENT_SECRET,authorize_endpoint=AUTHORIZE_ENDPOINT,token_endpoint=TOKEN_ENDPOINT,refresh_token_endpoint= TOKEN_ENDPOINT,revoke_token_endpoint=REVOKE_ENDPOINT)
          btnSigninGG = oauth2.authorize_button(
                    name="Login with Google",
                    icon="https://www.google.com.tw/favicon.ico",
                    redirect_uri="http://localhost:8501",
                    scope="openid profile email",
                    key="google",
                    use_container_width=True,
                    extras_params={"prompt": "consent", "access_type": "offline"},
                    pkce='S256',
                )
          
          if  btnSigninGG:
                    id_token = btnSigninGG["token"]["id_token"]
                    payload = id_token.split(".")[1]
                    payload += "=" * (-len(payload) % 4)
                    payload = json.loads(base64.b64decode(payload))
                    name = payload["name"]
                    link_picture = payload["picture"]
                    email = payload["email"]
                    st.session_state["auth"] = email
                    st.session_state["user_name"] = name
                    st.session_state["link_picture"] = link_picture
                    st.session_state["token"] = btnSigninGG["token"]                    
                    headers = {'Content-Type': 'application/json', 'accept': 'application/json'}
                    user_email = st.session_state["auth"] 
                    name_1 = st.session_state["user_name"]
                    link_picture1 = st.session_state["link_picture"]
                    url = f"{api}/default/create_firebase_user_google"
                    payload_url = {'email': user_email,"token_google": id_token}
                    requests.post(url,json=payload_url,headers=headers)
                    headers = {'Content-Type': 'application/json', 'accept': 'application/json'}
                    payload = {'email': user_email,'token_google':id_token}
                    api_endpoint = f"{api}/auth/login_google"
                    result = requests.post(api_endpoint, json=payload,headers=headers)
                    if result.status_code == 422:
                         st.toast("Unprocessable entity", icon='❌')
                    if result.status_code == 500:
                         st.toast("Internal server error", icon='❌')
                    if result.status_code == 200:
                            status = int(result.json()['status'])
                            result1 = result.json()['data']
                            if status != 200:
                              message = result1['message']
                              st.toast(message, icon='❌')
                            st.session_state["authenticated"] = True
                            token = result1["access_token"]
                            rf_token = result1["refresh_token"]
                            session_id = result1["session_id"]
                            url_isme = f"{api}/default/is_me"
                            user_data_isme = requests.get(url_isme,params={'token': token})
                            user_id = user_data_isme.json()['data']['user_id']
                            url = f'{api}/users/check_info_google'
                            params = {
                                'user_id': user_id
                                   }
                            headers = {
                                'accept': 'application/json'}
                            check_login = requests.get(url, headers=headers, params=params)
                            is_google = check_login.json()['data']['check']
                            headers = {"Authorization": f"Bearer {token}",'Content-Type': 'application/json', 'accept': 'application/json'}
                            url_info = f"{api}/default/info_user/{user_id}"
                            user_info_data = requests.get(url_info,headers=headers)
                            if int(user_info_data.json()['status']) == 500:
                                st.toast("Error", icon='❌')
                            if is_google == True:
                             data_user = user_info_data.json()['data']
                             uid = data_user["uid"]
                             email = data_user["email"]
                             name_1 = data_user["display_name"]
                             link_picture1 = data_user["photo_url"]
                            else:
                             data_user = user_info_data.json()['data']
                             uid = data_user["uid"]
                             email = data_user["email"]
                            user_info= {
                                "user_id": user_id,
                                "uid": uid,
                                "email": st.session_state["auth"] ,
                                "display_name": name_1,
                                "photo_url": link_picture1
                                  }
                            headers = {"Authorization": f"Bearer {token}", 'accept': 'application/json'}
                            url_update = f"{api}/users/update_user_info"
                            response = requests.put(url_update, json=user_info,headers=headers)
                            if int(response.json()['status']) == 500:
                                st.toast("Error", icon='❌')
                            controller.set('token_data',token,secure= True,same_site='strict')
                            controller.set('refresh_token',rf_token,secure= True,same_site='strict')
                            controller.set('session_id',session_id)
                            controller.set('login_google',True)
                            st.toast("Login success", icon='✅')
         except:
                    st.toast("Retry the function", icon='⚠️')           
if __name__ == "__main__":
    st.markdown(f"""
        <style>
        [data-testid="stAppViewContainer"] {{
         background-image: url("https://github.com/vonhuy1/KLTN_demo/blob/main/3%20(1).png?raw=true") ;
         background-size:cover;
         }}
        </style>
        """,unsafe_allow_html=True)
    
    css_st_bb = """
<style>
.st-bb {
    justify-content: center;
    color: #4050b0;
    font-weight:bold !important;
}
</style>
"""
    st.markdown(css_st_bb, unsafe_allow_html=True)
    css_st_emotion_cache_1aic7gq_p = """
   <style>
   .st-emotion-cache-1aic7gq p {
    word-break: break-word;
    font-size: 18px;
}
</style>
"""
    st.markdown(css_st_emotion_cache_1aic7gq_p, unsafe_allow_html=True)
    controller.set('token_data', None, secure= True,same_site='strict')
    controller.set('refresh_token',None,secure= True,same_site='strict')
    controller.set('session_id',None,secure= True,same_site='strict')
    controller.set('email',None,secure= True,same_site='strict')
    controller.set('login_google',None,secure= True,same_site='strict')
    st.session_state["authenticated"] = False
    main()
    if st.session_state.get("authenticated") == True:
        hide_multi_pages()
        render_welcome()
    else:
        hide_multi_pages()
        pass