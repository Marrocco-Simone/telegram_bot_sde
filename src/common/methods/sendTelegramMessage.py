import requests

# retrieve tokens from .env file
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

telegram_url = 'https://api.telegram.org/bot'+BOT_TOKEN

def sendTelegramMessage(chat_id: str, return_msg: str):
  '''send a message to a telegram chat'''
  r = requests.post(
    telegram_url+'/sendMessage', 
    json={
      'chat_id': chat_id, 
      'text': return_msg
    }
  )
  return r