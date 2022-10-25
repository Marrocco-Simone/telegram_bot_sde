import requests

# retrieve tokens from .env file
from dotenv import load_dotenv
import os
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

telegram_url = 'https://api.telegram.org/bot'+BOT_TOKEN

def sendDice(chat_id: str):
  '''send a dice animated emoji to a chat'''
  requests.post(
    telegram_url+'/sendDice', 
    json={
      'chat_id': chat_id
    }
  )