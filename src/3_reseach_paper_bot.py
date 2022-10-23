from time import sleep
import requests
from common.classes.classes import GetUpdatesResponse, Update
from common.methods.parseUpdate import parseUpdate
from common.classes.core_ac_classes import CoreACSearchResponse

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
  update_info = parseUpdate(update)

  r = requests.get(
    core_ac_url, 
    params={
      'q': update_info["message"],
      'limit': 30
    }, 
    headers = {"Authorization": "Bearer "+CORE_AC_TOKEN}
  )
  core_ac_response: CoreACSearchResponse = r.json()

  for s in core_ac_response['results']:
    return_msg = s['abstract']
    requests.post(
      telegram_url+'/sendMessage', 
      json={
        'chat_id': update_info["chat_id"], 
        'text': return_msg
      }
    )

print('Server online. Waiting...\n')
# id of the last parsed message
last_update = 0
while True:
  r = requests.get(
    telegram_url+'/getUpdates', 
    params={
      'offset': last_update
    }
  )
  response: GetUpdatesResponse = r.json()

  if len(response['result']) > 0:
    for update in response['result']:
      parse_response(update)
      last_update = update['update_id']+1

  sleep(1)