from time import sleep
import requests
from common.classes import GetUpdatesResponse, SendMessageResponse, Update
from common.core_ac_classes import CoreACSearchResponse

# retrieve tokens from .env file
from dotenv import load_dotenv
import os
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
CORE_AC_TOKEN = os.getenv('CORE_AC_TOKEN')

# urls
telegram_url = 'https://api.telegram.org/bot'+BOT_TOKEN
core_ac_url = 'https://api.core.ac.uk/v3/search/works/'

def parse_response(update: Update):
  sender = update['message']['chat']['username']
  message = update['message']['text']
  chat_id = update['message']['chat']['id']

  log = sender+' says: '+message
  print(log)

  r = requests.get(
    core_ac_url, 
    params={
      'q': message,
      'limit': 30
    }, 
    headers = {"Authorization": "Bearer "+CORE_AC_TOKEN}
  )
  core_ac_response: CoreACSearchResponse = r.json()

  for s in core_ac_response['results']:
    return_msg = s['abstract']
    requests.post(telegram_url+'/sendMessage', json={'chat_id': chat_id, 'text': return_msg})

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