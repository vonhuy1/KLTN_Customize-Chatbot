import nest_asyncio
from uvicorn import run
nest_asyncio.apply() 
from pyngrok import ngrok
from fastapi import FastAPI
from dotenv import load_dotenv
import os
load_dotenv()
NGROK_STATIC_DOMAIN = ""
NGROK_TOKEN = ""
app = FastAPI()

if __name__ == "__main__":
    ngrok.set_auth_token(NGROK_TOKEN)
    ngrok_tunnel = ngrok.connect(8000, domain=NGROK_STATIC_DOMAIN)
    print('Public URL:', ngrok_tunnel.public_url)
    run(app, port=8000)