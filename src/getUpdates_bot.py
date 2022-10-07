from time import sleep
from dotenv import load_dotenv
import os

from common.classes import Response, Result
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

import requests

# pass the returned object of requests.get r as r.json()
def parse_response(result: Result):
  sender = result['message']['chat']['username']
  message = result['message']['text']
  print(sender+' says: '+message)

last_update = 0
while True:
  url = 'https://api.telegram.org/bot'+BOT_TOKEN+'/getUpdates'
  r = requests.get(url, params={'offset': last_update})
  response: Response = r.json()

  if len(response['result']) > 0:
    for result in response['result']:
      parse_response(result)
      last_update = result['update_id']+1

  sleep(1)