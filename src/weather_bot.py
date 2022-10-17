from time import sleep
from dotenv import load_dotenv
import os

from common.classes import GetUpdatesResponse, SendMessageResponse, Update
from common.weather_classes import MapBoxResponse, WeatherStackResponse
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
WEATHERSTACK_TOKEN = os.getenv('WEATHERSTACK_TOKEN')
MAPBOX_TOKEN = os.getenv('MAPBOX_TOKEN')

import requests

telegram_url = 'https://api.telegram.org/bot'+BOT_TOKEN
weatherstack_url = 'http://api.weatherstack.com/current'
mapbox_url = 'https://api.mapbox.com/geocoding/v5/mapbox.places/'

def execute_command(chat_id: str, sender: str, command: str, msg_args: str):  
  msg = 'This command is not currently supported'

  if len(msg_args) == 0:
    msg = 'Add some arguments'
  elif command == 'weather':
    r = requests.get(weatherstack_url, params={
      'query': msg_args,
      'access_key': WEATHERSTACK_TOKEN
    })
    weather_obj: WeatherStackResponse = r.json()
    msg = \
      str(weather_obj['location']['name']) + ': ' + \
      str(weather_obj['current']['temperature']) + \
      ', it feels like ' + str(weather_obj['current']['feelslike']) + \
      ' and with precipitations ' + str(weather_obj['current']['precip'])
  elif command == 'geolocate':
    r = requests.get(mapbox_url + msg_args + '.json', params={
      'limit': '10',
      'access_token': MAPBOX_TOKEN
    })
    geolocate_obj: MapBoxResponse = r.json()
    msg = ''
    for feature in geolocate_obj['features']:
      msg = msg + \
        str(feature['place_name']) + ': ' + \
        str(feature['center'][1]) + ', ' + \
        str(feature['center'][0]) + '\n\n'

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