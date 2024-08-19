import streamlit as st
import time,requests
import smtplib
from streamlit_cookies_controller import CookieController
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from streamlit_extras.stylable_container import stylable_container
controller = CookieController()
from dotenv import load_dotenv
import os
load_dotenv()
API = os.getenv("BE_API")
EMAIL= os.getenv('EMAIL')
PASSWORD=os.getenv('PASSWORD')
EMAIL_DOMAIN=os.getenv('EMAIL_DOMAIN')
api = API
token = controller.get('token_data')
session_id_now = controller.get('session_id')
import datetime
from pages.page1 import support_function as sf
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
                user_info_data = requests.get(url_info,headers=headers)
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

def check_state_login():
    session_id_now = controller.get('session_id')
    user_id = st.session_state.get("user_id")
    api_url = f"{api}/users/check_state_login"
    params = {
    'user_id': user_id,
    'session_id_now': session_id_now
}   
    response = requests.get(api_url, params=params)
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
                            message = "Bad GateWay"
                            st.toast(f"{message}", icon='❌')
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

def send_feedback_email(user_email, feedback_content):
    check_state_login()
    user_html_body = f"""
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
                <h2>Feedback Received - MyChatBot</h2>
            </div>
            <div class="content">
                <p>Hello, {user_email}</p>
                <p>Thank you for your feedback!</p>
                <p>Your feedback:</p>
                <p class="otp-code">{feedback_content}</p>
                <p>We appreciate your input and will take it into consideration to improve our services.</p>
                <p>Best regards,<br>Vo Nhu Y</p>
            </div>
            <div class="footer">
                <p>If you have any further questions, please feel free to contact us.</p>
                <p>Contact us at <a href="mailto:20133118@student.hcmute.edu.vn">20133118@student.hcmute.edu.vn</a></p>
            </div>
        </div>
    </body>
    </html>
    """
    
    admin_html_body = f"""
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
                <h2>New Feedback Received</h2>
            </div>
            <div class="content">
                <p>User: {user_email}</p>
                <p>Feedback content:</p>
                <p class="otp-code">{feedback_content}</p>
                <p>Please review this feedback and take the necessary actions.</p>
                <p>Best regards,<br>MyChatBot System</p>
            </div>
            <div class="footer">
                <p>If you have any further questions, please feel free to contact us.</p>
                <p>Contact us at <a href="mailto:20133118@student.hcmute.edu.vn">20133118@student.hcmute.edu.vn</a></p>
            </div>
        </div>
    </body>
    </html>
    """
    send_email(
        subject="Thank you for your feedback",
        body=user_html_body,
        to_email=user_email
    )
    send_email(
        subject="New Feedback Received",
        body=admin_html_body,
        to_email=EMAIL_DOMAIN
    )
    st.toast(f'Send feedback success', icon='✅')
    time.sleep(3)

def show_contacts():
    st.header("Contact", divider='orange')
    st.subheader("**If necessary, please contact us. Please contact information of the following methods.**")
    btn1, btn2 = st.columns(2)
    with btn1:
        st.write("Name: Vo Nhu Y. (Team leader)")
        st.write("Email: 20133118@student.hcmute.edu.vn")
        st.write("Phone: +84 769674810")
    with btn2:
        st.write("Name: Nguyen Quang Phuc. (Member)")
        st.write("Email: 20133080@student.hcmute.edu.vn")
        st.write("Phone: +84 905813065")  

    st.header("Feedback", divider='blue')
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
    st.markdown(css_12,unsafe_allow_html=True)
    feed_back = st.text_area(":blue[Content]",placeholder="Please enter information to respond")
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
           "btn_sendres",
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
                   btn_response= st.button("Send Feedback",key = "btnsend_feedback")
    if btn_response:
        email = st.session_state['email']
        send_feedback_email(email,feed_back)  