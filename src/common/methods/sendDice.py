import requests

# retrieve tokens from .env file
from dotenv import load_dotenv
import os
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

# urls
telegram_url = 'https://api.telegram.org/bot'+BOT_TOKEN

def sendDice(chat_id: str):
  requests.post(
    telegram_url+'/sendDice', 
    json={
      'chat_id': chat_id
    }
  )