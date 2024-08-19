import streamlit as st
import time
import requests
from streamlit_extras.stylable_container import stylable_container
import re
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
load_dotenv()
API = os.getenv("BE_API")
api = API
def send_email(subject, body, to_email):
    from_email = ""
    from_password = ""
    smtp_server = ""
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

def send_verification_reset(to_email, otp_code):
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
                background-color: #149c55f7;
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
                background-color: #c2d31447;
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
                <h2>Reset Password Account</h2>
            </div>
            <div class="content">
                <p>Hello, {to_email}</p>
                <p>This is new password reset:</p>
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
        subject="Reset Password Account",
        body=html_body,
        to_email=to_email
    )
    

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
                <h2>Verify Email Reset Password</h2>
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
        subject="Verify Email Reset Passord",
        body=html_body,
        to_email=to_email
    )
    
def check(email):
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False
if __name__ == "__main__":
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
 css_st_font = """
<style>
.st-emotion-cache-13jyg6u h1 {
    font-size: 16px;
    font-weight: bold;
    font-family: inherit;
    color: red;
}
</style>
"""
 st.markdown(css_st_font, unsafe_allow_html=True)
 st.markdown(f"""
        <style>
        [data-testid="stAppViewContainer"] {{
         background-image: url("https://github.com/vonhuy1/KLTN_demo/blob/main/3%20(1).png?raw=true") ;
         background-size:cover;
         }}
        </style>
        """,unsafe_allow_html=True)
 
 with st.form(key='forgot',border=True):
         
         @st.experimental_dialog("Verify Email")
         def verify_email():
                st.title("Please check your email and enter the OTP we have sent. The OTP is valid for 15 minutes.")
                otp = st.text_input(":blue[OTP]", key="user_otp", placeholder="Enter Your OTP")
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
                  else:
                    email_reset = st.session_state["email_reset"]
                    headers = {'Content-Type': 'application/json', 'accept': 'application/json'}
                    payload2 = {'email': email_reset,'otp': otp}
                    api_endpoint2 = f"{api}/otp/verify_otp_reset_password"
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
                        newpassword = res.json()['newpassword']
                        send_verification_reset(email_reset,newpassword)
                        message = "Reset password success. Please check email!"
                        st.toast(message, icon='✅')
                        time.sleep(1)
                        st.markdown('<meta http-equiv="refresh" content="0;URL=http://localhost:8501/login" />', unsafe_allow_html=True)
                     else:
                        message = data_verify['message']
                        st.toast(message, icon='❌')
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
         css = """
<style>
h3 {
    font-family: "Source Sans Pro", sans-serif;
    font-weight: 600;
    color: #D35400;
    letter-spacing: -0.005em;
    display: flex;
    padding: 0.5rem 0px 1rem;
    margin: 0px;
    line-height: 1.2;
    justify-content: center;
    boder: 2px;
    font-weight: bold !important;
    margin-top: -40px;

}
</style>
"""


         st.markdown(css, unsafe_allow_html=True)
         st.subheader('Forgot Password')
         css = """
<style>
.st-emotion-cache-1jmvea6 p {
    word-break: break-word;
    margin-bottom: 0px;
    font-size: 20px !important;
    border: 2px;
    font-weight: bold !important;
    color: #D35400;
    
}
</style>
"""
         st.markdown(css, unsafe_allow_html=True)
         email = st.text_input('Email Address', key="email_forgot",placeholder="abcd@gmail.com")
         with stylable_container(
           "send",
         css_styles="""
          button {
           background: -webkit-linear-gradient(#ff520b, #fdffd0);
           color: black;
           width: 120px;
           border-radius: 9px;
           boder: 2px;
           display:flex;
           align-items: center;
           justify-content: center;
           }""",
        ):
                   btnForgot= st.form_submit_button("Send")
         if btnForgot:
          if email:
           if check(email) == True:
            headers = {'Content-Type': 'application/json', 'accept': 'application/json'}
            payload = {'email': email}
            api_endpoint = f"{api}/users/reset_password"
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
            otp = result.json()['otp']
            st.session_state["email_reset"] = ""
            if result.status_code == 200:
             if status == 200:
                  st.session_state["email_reset"] = email
                  send_verification_email(email,otp)
                  time.sleep(1.5)
                  verify_email()
             if status == 500:
                  res = result.json()['data']
                  message = res["message"]
                  st.toast(message, icon='❌')
             if status == 415:
                  res = result.json()['data']
                  message = res["message"]
                  st.toast(message, icon='❌')
             if status == 404:
                  res = result.json()['data']
                  message = res["message"]
                  st.toast(message, icon='❌')
             if status == 400:
                  res = result.json()['data']
                  message = res["message"]
                  st.toast(message, icon='❌')
            if result.status_code == 500:
                 st.toast("Server Error", icon='❌')
            if result.status_code == 422:
                 st.toast(" Unprocessable Entity", icon='❌')
           else:
                 st.toast("Email in valid", icon='❌')
          else:
                st.toast("Email is None", icon='❌')

 with stylable_container(
           "green",
         css_styles="""
          button {
           background: -webkit-linear-gradient(#41aa96, #eeefcc);
           color: black;
           width: 280px;
           border-radius: 10px;
           boder: 2px;

           }""",
        ):
                   btnBack = st.button("🔙 Back")
 if btnBack:
         st.toast("Back page Login", icon='✅')
         time.sleep(1)
         st.markdown('<meta http-equiv="refresh" content="0;URL=http://localhost:8501/login" />', unsafe_allow_html=True)
