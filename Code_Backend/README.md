# Backend KLTN
Demo Front End:

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://pychatbot20133.streamlit.app/)


Yet another chatgpt web made by streamlit!

Online Demo Backend Server on [Huggingface](https://kltn20133118-pychatbot.hf.space/docs)

## Feature

- Log in by Email, Password; Login by Google
- Sign Up
- Generate Question from document
- Chat with file pdf, txt, csv, xlsx, docx, json, pptx
- Upload file, delete file, delete all file, get list file, extract file to vector database
- Upload image(png,jpg,jpeg) with [Cloudinary](https://cloudinary.com/)
- Save file with [Dropbox](https://www.dropbox.com/home)
- Authenticate with [Firebase](https://console.firebase.google.com/u/0/)
- SQL
- Docker, load balancer with nginx

## Start Server Local Docker

1. Python3 environment ready. Please choose python version `3.10 to 3.11.2`
2. First, you need to fill in the environment variables: [CLOUDINARY](https://cloudinary.com/developers), [COHERE](https://dashboard.cohere.com/api-keys), `MYSQL` ,[DROPBOX](https://www.dropbox.com/developers),[GOOGLE_API_STUDIO](https://aistudio.google.com/app/apikey), [GOOGLE_OAUTH2(CLIENT_ID)](https://console.cloud.google.com/apis/credentials?), [GROQ](https://console.groq.com/keys) in the external .env file and in the app/.env
3. In the app folder, please add the [FireBase](https://console.firebase.google.com/u/0/project/cogent-octane-384105/settings/general/web:NjAyOGY0YTktNjg1OC00NTQ0LWJkNmItMTdhN2EwMmI1NmUy) certificate after the path `/app/certificate`,`/app/service/app`. Note: Rename the certificate files to `firebase_certificate.json`, Or just put your firebase certificate in those files
4. Log in to mysql on your computer and use the `create_pychatbot.db` file to create the database, then fill in the necessary fields in the `/app/repository/ConfigDatabase.py` file. Note: If you are using an online server, you will need an SSL certificate.
5. Install and setup Docker on your computer. In `docker-compose.yaml` file, you adjust the path properties on the computer in volumes/device.
6. Install the library using the requirements.txt file. Type the command `python -m pip install -r requirements.txt` into the Terminal.
7. In Terminal or Command Prompt or Windows PowerShell, type `docker-compose up --build` to run Docker.
8. If you start Docker successfully, access the link http://localhost:8000/docs to use the API on Swagger UI.

## Start Server Local No Docker
1. Python3 environment ready. Please choose python version `3.10 to 3.11.2`
2. First, you need to fill in the environment variables: [CLOUDINARY](https://cloudinary.com/developers), [COHERE](https://dashboard.cohere.com/api-keys), `MYSQL` ,[DROPBOX](https://www.dropbox.com/developers),[GOOGLE_API_STUDIO](https://aistudio.google.com/app/apikey), [GOOGLE_OAUTH2(CLIENT_ID)](https://console.cloud.google.com/apis/credentials?), [GROQ](https://console.groq.com/keys) in the external .env file and in the app/.env
3. In the app folder, please add the FireBase certificate after the path `/app/certificate`,`/app/service/app`. Note: Rename the certificate files to `firebase_certificate.json`, Or just put your firebase certificate in those files
4. Log in to mysql on your computer and use the `create_pychatbot.db` file to create the database, then fill in the necessary fields in the `/app/repository/ConfigDatabase.py` file. Note: If you are using an online server, you will need an SSL certificate.
5. Install the library using the requirements.txt file. Type the command `python -m pip install -r requirements.txt` into the Terminal.
6. In Terminal or Command Prompt or Windows PowerShell, move into app folder and type the command `python run_main_no_docker.py` to run.
7. If you start docker successfully, access the link http://localhost:9090/docs to use the API on Swagger UI

## Hosting Server Online with Ngrok
1. Make sure that the server is running in 1 of the 2 modes mentioned in the name.
2. Replace variables [NGROK_TOKEN_DOMAIN](https://dashboard.ngrok.com/cloud-edge/domains), [NGROK_TOKEN](https://dashboard.ngrok.com/get-started/your-authtoken) in .env
3. In Terminal or Command Prompt or Windows PowerShell  type the command `python start_server.py`
4. Access `NGROK_STATIC_DOMAIN/docs` to use server