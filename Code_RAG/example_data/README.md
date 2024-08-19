# pychatbot

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://pychatbot1.streamlit.app/)

Yet another chatgpt web made by streamlit!

Online Demo Server BackEnd on [Huggingface](https://kltn20133118-pychatbot.hf.space/docs)

## Feature
 
- Multi chats
- Support file pdf, docx, txt, pptx, csv, xlsx, json, md
- Different Role(Prompt) Selection
- Chat name editable
- Delete chats
- Export conversion to markdown
- Support downloading all tables in answer to excel
- Support streaming
- Authenticate
- Regenerate
- Stop generating while streaming
- Login Email, Login Google
- UpLoaf File, Update UserInforMation
- Contact/FeedBack
- Join group community

## Start

1. Python3 environment ready. Please choose python version `3.10 to 3.11.2`
2. First, you need to fill in the .env variables: `BE_API`(The link is taken from the BackEnd server when running the code), `EMAIL`,`PASSWORD_EMAIL`,`EMAIL_DOMAIN` ,[GOOGLE_OAUTH2(CLIENT_ID)(CLIENT_SECRET)](https://console.cloud.google.com/apis/credentials?), note that these properties are the same as the CLIENT_ID in the BackEnd side's.
3. Install requirement. `python -m pip install -r requirements.txt`
4. Launch. `streamlit run login.py`
