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

stored_data: str = ''

def send_dice(chat_id: str):
  requests.post(telegram_url+'/sendDice', json={'chat_id': chat_id})

def execute_command(chat_id: str, sender: str, command: str, msg_args: str):  
  global stored_data
  msg = 'This command is not currently supported'

  if command == 'dice':
    send_dice(chat_id)
    return

  if command == 'start' or command == 'help':
    msg = 'Welcome to our bot\n' + \
      'Possible commands:\n' + \
      '/start or /help: info about the bot\n' + \
      '/dice: throw a dice\n' + \
      '/get_stored: get your stored data\n' + \
      '/change_stored [arg]: change your stored data'
  if command == 'get_stored':
    msg = 'You have stored: ' + stored_data
  if command == 'change_stored':
    stored_data = msg_args
    msg = 'You have stored: ' + stored_data

  r = requests.post(telegram_url+'/sendMessage', json={'chat_id': chat_id, 'text': msg})
  # response: SendMessageResponse = r.json()
  # msg_sent = response['result']['text']
  # recipient = response['result']['chat']['username']
  # print('you sent back to '+recipient+': {'+msg_sent+'}')

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