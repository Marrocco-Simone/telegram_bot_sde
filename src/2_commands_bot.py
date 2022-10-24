import requests
from common.methods.parseUpdate import UpdateInfo
from common.methods.sendTelegramMessage import sendTelegramMessage
from common.methods.startServer import startServerPolling

# retrieve tokens from .env file
from dotenv import load_dotenv
import os
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

# urls
telegram_url = 'https://api.telegram.org/bot'+BOT_TOKEN

stored_data: str = ''

def send_dice(chat_id: str):
  requests.post(
    telegram_url+'/sendDice', 
    json={
      'chat_id': chat_id
    }
  )

def execute_command(chat_id: str, sender: str, command: str, msg_args: str):  
  global stored_data
  return_msg = 'This command is not currently supported'

  if command == 'dice':
    send_dice(chat_id)
    return

  if command == 'start' or command == 'help':
    return_msg = '''
Welcome to our bot
Possible commands:
/start or /help: info about the bot
/dice: throw a dice
/get_stored: get your stored data
/change_stored [arg]: change your stored data\
'''

  if command == 'get_stored':
    return_msg = 'You have stored: ' + stored_data

  if command == 'change_stored':
    stored_data = msg_args
    return_msg = 'You have stored: ' + stored_data

  sendTelegramMessage(['chat_id'], return_msg)

def parse_response(update_info: UpdateInfo):
  if update_info["message"].startswith('/'):
    # get first word after /, so the command
    command = update_info["message"].split(' ')[0].lstrip('/')
    # get the rest of the message
    msg_args = update_info["message"].replace('/'+command, '', 1)
    execute_command(update_info["chat_id"], update_info["sender"], command, msg_args)

startServerPolling(parse_response)
