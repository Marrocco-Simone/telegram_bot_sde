import requests
from common.methods.getResearchPapers import getResearchPapers
from common.methods.parseUpdate import UpdateInfo
from common.methods.startServer import startServerPolling

# retrieve tokens from .env file
from dotenv import load_dotenv
import os
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
CORE_AC_TOKEN = os.getenv('CORE_AC_TOKEN')

# urls
telegram_url = 'https://api.telegram.org/bot'+BOT_TOKEN

def parse_response(update_info: UpdateInfo):
  core_ac_response = getResearchPapers(update_info, CORE_AC_TOKEN)

  # send a message for each abstract received
  for s in core_ac_response['results']:
    return_msg = s['abstract']
    requests.post(
      telegram_url+'/sendMessage', 
      json={
        'chat_id': update_info["chat_id"], 
        'text': return_msg
      }
    )

startServerPolling(parse_response)