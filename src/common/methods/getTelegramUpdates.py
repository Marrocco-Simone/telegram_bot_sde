import requests
from common.classes.classes import GetUpdatesResponse

# retrieve tokens from .env file
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

telegram_url = f'https://api.telegram.org/bot{BOT_TOKEN}'

def getTelegramUpdates(last_update: int):
  '''get the recent updates from telegram'''
  r = requests.get(
      f'{telegram_url}/getUpdates', 
      params={
        'offset': last_update,
        'allowed_updates':['message'],
        # we only want messages sent by the user (we ignore everything else)
        'timeout': 0
        # Timeout in seconds for long polling.
        # It should be set to a higher value if the bot is deployed, 
        # but for testing purposes it is ok to keep it to 0
      }
    )
  response: GetUpdatesResponse = r.json()
  return response