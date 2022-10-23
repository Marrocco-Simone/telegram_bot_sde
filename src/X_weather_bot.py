import requests
from common.methods.parseUpdate import UpdateInfo
from common.methods.startServer import startServerPolling
from common.classes.weather_classes import MapBoxOutput, MapBoxResponse, WeatherStackOutput, WeatherStackResponse
from typing import List

# retrieve tokens from .env file
from dotenv import load_dotenv
import os
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
WEATHERSTACK_TOKEN = os.getenv('WEATHERSTACK_TOKEN')
MAPBOX_TOKEN = os.getenv('MAPBOX_TOKEN')

# urls
telegram_url = 'https://api.telegram.org/bot'+BOT_TOKEN
weatherstack_url = 'http://api.weatherstack.com/current'
mapbox_url = 'https://api.mapbox.com/geocoding/v5/mapbox.places/'

def call_weather_api(args) -> WeatherStackOutput:
  r = requests.get(
    weatherstack_url, 
    params={
      'query': args,
      'access_key': WEATHERSTACK_TOKEN
    }
  )
  weather_obj: WeatherStackResponse = r.json()
  weather_output: WeatherStackOutput = {
    'name': weather_obj['location']['name'],
    'temperature': weather_obj['current']['temperature'],
    'feelslike': weather_obj['current']['feelslike'],
    'precip': weather_obj['current']['precip']
  }
  return weather_output

def print_weather_output(weather_output: WeatherStackOutput):
  return \
    str(weather_output['name']) + ': ' + \
    str(weather_output['temperature']) + \
    ', it feels like ' + str(weather_output['feelslike']) + \
    ' and with precipitations ' + str(weather_output['precip'])

def call_geolocate_api(args: str) -> List[MapBoxOutput]:
  r = requests.get(
    mapbox_url + args + '.json', 
    params={
      'limit': '10',
      'access_token': MAPBOX_TOKEN
    }
  )
  geolocate_obj: MapBoxResponse = r.json()
  geolocate_output: List[MapBoxOutput] = []
  for feature in geolocate_obj['features']:
    geolocate_output.append({
      'name': feature['place_name'],
      'latitude': feature['center'][1],
      'longitude': feature['center'][0],
    })
  return geolocate_output

def get_coordinates_from_mapbox_output(mapbox_output: MapBoxOutput):
  return str(mapbox_output['latitude']) + ', ' + str(mapbox_output['longitude'])

def print_geolocate_output(geolocate_output: List[MapBoxOutput]):
  msg = ''
  for out in geolocate_output:
    msg = msg + \
      str(out['name']) + ': ' + \
      get_coordinates_from_mapbox_output(out) + '\n\n'
  return msg

def search_city_weather(chat_id: str, message: str):
  geolocate_output = call_geolocate_api(message)
  coordinates = get_coordinates_from_mapbox_output(geolocate_output[0])
  weather_output = call_weather_api(coordinates)
  msg = print_weather_output(weather_output)

  requests.post(
    telegram_url+'/sendMessage', 
    json={
      'chat_id': chat_id, 
      'text': msg
    }
  )

def execute_command(chat_id: str, sender: str, command: str, msg_args: str):  
  msg = 'This command is not currently supported'

  if len(msg_args) == 0:
    msg = 'Add some arguments'
  elif command == 'weather':
    weather_output = call_weather_api(msg_args)
    msg = print_weather_output(weather_output)
  elif command == 'geolocate':
    geolocate_output = call_geolocate_api(msg_args)
    msg = print_geolocate_output(geolocate_output)

  requests.post(
    telegram_url+'/sendMessage', 
    json={
      'chat_id': chat_id, 
      'text': msg
    }
  )

def parse_response(update_info: UpdateInfo):
  if update_info["message"].startswith('/'):
    command = update_info["message"].split(' ')[0].lstrip('/')
    msg_args = update_info["message"].replace('/'+command, '', 1)
    execute_command(update_info["chat_id"], update_info["sender"], command, msg_args)
  else:
    search_city_weather(update_info["chat_id"], update_info["message"])

startServerPolling(parse_response)
