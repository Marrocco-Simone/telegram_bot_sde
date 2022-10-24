from time import sleep
import requests
from typing import Callable
from common.methods.parseUpdate import UpdateInfo, parseUpdate
from common.classes.classes import GetUpdatesResponse

# retrieve tokens from .env file
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

# urls
telegram_url = f'https://api.telegram.org/bot{BOT_TOKEN}'

def startServerPolling(parse_response: Callable[[UpdateInfo], None]):
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
        update_info = parseUpdate(update)
        parse_response(update_info)
        last_update = update['update_id']+1

    sleep(1)
