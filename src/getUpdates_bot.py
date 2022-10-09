from time import sleep
from dotenv import load_dotenv
import os

from common.classes import GetUpdatesResponse, SendMessageResponse, Update
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

import requests

telegram_url = 'https://api.telegram.org/bot'+BOT_TOKEN

def parse_response(update: Update):
  sender = update['message']['chat']['username']
  message = update['message']['text']
  log = sender+' says: '+message
  print(log)

  chat_id = update['message']['chat']['id']
  return_msg = 'Hi '+sender+', you told me: '+message
  r = requests.post(telegram_url+'/sendMessage', json={'chat_id': chat_id, 'text': return_msg})
  
  response: SendMessageResponse = r.json()
  msg_sent = response['result']['text']
  recipient = response['result']['chat']['username']
  print('you sent back to '+recipient+': {'+msg_sent+'}')

last_update = 0
while True:
  r = requests.get(telegram_url+'/getUpdates', params={'offset': last_update})
  response: GetUpdatesResponse = r.json()

  if len(response['result']) > 0:
    for update in response['result']:
      parse_response(update)
      last_update = update['update_id']+1

  sleep(1)