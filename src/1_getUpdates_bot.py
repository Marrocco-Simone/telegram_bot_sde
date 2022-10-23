import requests
from common.classes.classes import  SendMessageResponse
from common.methods.parseUpdate import UpdateInfo
from common.methods.startServer import startServerPolling

# retrieve tokens from .env file
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

# urls
telegram_url = 'https://api.telegram.org/bot'+BOT_TOKEN

def parse_response(update_info: UpdateInfo):
  return_msg = f'Hi {update_info["sender"]}, you told me: {update_info["message"]}'
  r = requests.post(
    telegram_url+'/sendMessage', 
    json={
      'chat_id': update_info['chat_id'], 
      'text': return_msg
    }
  )
  
  response: SendMessageResponse = r.json()
  msg_sent = response['result']['text']
  recipient = response['result']['chat']['username']
  print('you sent back to '+recipient+': {'+msg_sent+'}')

startServerPolling(parse_response)
