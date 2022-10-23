from time import sleep
import requests
from common.classes import GetUpdatesResponse, SendMessageResponse, Update

# retrieve tokens from .env file
from dotenv import load_dotenv
import os
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

# urls
telegram_url = 'https://api.telegram.org/bot'+BOT_TOKEN

def parse_response(update: Update):
  chat_id = update['message']['chat']['id']
  sender = update['message']['chat']['username']
  message = update['message']['text']
  log = f"{sender} says: {message}"
  print(log)

  return_msg = 'Hi '+sender+', you told me: '+message
  r = requests.post(telegram_url+'/sendMessage', json={'chat_id': chat_id, 'text': return_msg})
  
  response: SendMessageResponse = r.json()
  msg_sent = response['result']['text']
  recipient = response['result']['chat']['username']
  print('you sent back to '+recipient+': {'+msg_sent+'}')

print('Server online. Waiting...\n')
# id of the last parsed message
last_update = 0
while True:
  r = requests.get(telegram_url+'/getUpdates', params={'offset': last_update})
  response: GetUpdatesResponse = r.json()

  if len(response['result']) > 0:
    for update in response['result']:
      parse_response(update)
      last_update = update['update_id']+1

  sleep(1)