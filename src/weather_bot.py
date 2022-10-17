from time import sleep
from dotenv import load_dotenv
import os

from common.classes import GetUpdatesResponse, SendMessageResponse, Update
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
WEATHERSTACK_TOKEN = os.getenv('WEATHERSTACK_TOKEN')
MAPBOX_TOKEN = os.getenv('MAPBOX_TOKEN')

import requests

telegram_url = 'https://api.telegram.org/bot'+BOT_TOKEN
weatherstack_url = 'http://api.weatherstack.com/current'
mapbox_url = 'https://api.mapbox.com/geocoding/v5/mapbox.places/'

stored_data: str = ''

def execute_command(chat_id: str, sender: str, command: str, msg_args: str):  
  global stored_data
  msg = 'This command is not currently supported'

  if command == 'weather':
    r = requests.get(weatherstack_url, params={
      'query': '46.07,11.13',
      'access_key': WEATHERSTACK_TOKEN
    })
    msg = r.json()
  if command == 'geolocate':
    r = requests.get(mapbox_url + 'Trento' + '.json', params={
      'limit': '1',
      'access_token': MAPBOX_TOKEN
    })
    msg = r.json()

  requests.post(telegram_url+'/sendMessage', json={'chat_id': chat_id, 'text': msg})

def parse_response(update: Update):
  chat_id = update['message']['chat']['id']

  sender = update['message']['chat']['username']
  message = update['message']['text']
  log = sender+' says: '+message
  print(log)

  if message.startswith('/'):
    command = message.split(' ')[0].lstrip('/')
    msg_args = message.replace('/'+command, '', 1)
    execute_command(chat_id, sender, command, msg_args)

print('Server online. Waiting...\n')
last_update = 0
while True:
  r = requests.get(telegram_url+'/getUpdates', params={'offset': last_update})
  response: GetUpdatesResponse = r.json()

  if len(response['result']) > 0:
    for update in response['result']:
      parse_response(update)
      last_update = update['update_id']+1

  sleep(1)