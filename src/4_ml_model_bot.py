from time import time
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
HUGGING_FACE_TOKEN = os.getenv('HUGGING_FACE_TOKEN')

# urls
telegram_url = 'https://api.telegram.org/bot'+BOT_TOKEN
huggin_face_url = 'https://api-inference.huggingface.co/models/google/bigbird-pegasus-large-pubmed'

def parse_response(update_info: UpdateInfo):
  start = time()

  core_ac_response = getResearchPapers(update_info, CORE_AC_TOKEN)

  abstracts_text = ""
  try:
    for s in core_ac_response['results']:
      abstracts_text += f"{s['abstract']}\n"
  except:
    print(f'crashed core ac api. Reason: {core_ac_response["message"]}')
    return_msg = f'Sorry, request failed at CoreAc API. Reason: {core_ac_response["message"]}. Retry'
    requests.post(
      telegram_url+'/sendMessage', 
      json={
        'chat_id': update_info["chat_id"], 
        'text': return_msg
      }
    )
    return
  print(f'CoreAc responded with {len(core_ac_response["results"])} results, out of {core_ac_response["totalHits"]}')
  print(f"lenght of the abstract composition: {len(abstracts_text)}")

  hugging_face_response = requests.post(
    huggin_face_url, 
    headers={
      "Authorization": f"Bearer {HUGGING_FACE_TOKEN}"
    }, 
    json=abstracts_text
  )
  hugging_face_obj = hugging_face_response.json()
  print('HuggingFace responded')

  try:
    return_msg = hugging_face_obj[0]['summary_text']
    requests.post(
      telegram_url+'/sendMessage', 
      json={
        'chat_id': update_info["chat_id"], 
        'text': return_msg
      }
    )
  except:
    print(f"crashed hugging face api. Reason: {hugging_face_obj['error']}")
    return_msg = f"\
      Sorry, request failed at HuggingFace API. Reason: {hugging_face_obj['error']}. Retry"
    requests.post(
      telegram_url+'/sendMessage', 
      json={
        'chat_id': update_info["chat_id"], 
        'text': return_msg
      }
    )
    return

  end = time()
  print(f"request served in {end-start} s")

startServerPolling(parse_response)
