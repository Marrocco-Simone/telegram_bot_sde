import os

import requests
# retrieve tokens from .env file
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

telegram_url = 'https://api.telegram.org/bot' + BOT_TOKEN


def sendTelegramMessage(chat_id: str, return_msg: str):
    '''send a message to a telegram chat'''
    # the endpoint to use is /sendMessage
    # the json body has two fields: 'chat_id' and 'text'

    requests.post(
        telegram_url + '/sendMessage',
        json={
            'chat_id': chat_id,
            'text': return_msg
        }
    )
