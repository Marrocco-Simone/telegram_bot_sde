from time import sleep, time
import requests
from common.classes.classes import GetUpdatesResponse, Update
from common.methods.parseUpdate import parseUpdate
from common.classes.core_ac_classes import CoreACSearchResponse

# retrieve tokens from .env file
from dotenv import load_dotenv
import os
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
CORE_AC_TOKEN = os.getenv('CORE_AC_TOKEN')
HUGGING_FACE_TOKEN = os.getenv('HUGGING_FACE_TOKEN')

# urls
telegram_url = 'https://api.telegram.org/bot'+BOT_TOKEN
core_ac_url = 'https://api.core.ac.uk/v3/search/works/'
huggin_face_url = 'https://api-inference.huggingface.co/models/google/bigbird-pegasus-large-pubmed'

def parse_response(update: Update):
  update_info = parseUpdate(update)

  start = time()

  r = requests.get(
    core_ac_url, 
    params={
      'q': update_info["message"],
      'limit': 5
    }, 
    headers = {"Authorization": f"Bearer {CORE_AC_TOKEN}"}
  )
  core_ac_response: CoreACSearchResponse = r.json()

  abstracts_text = ""
  try:
    for s in core_ac_response['results']:
      abstracts_text += s['abstract'] + "\n"
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

print('Server online. Waiting...\n')
# id of the last parsed message
last_update = 0
while True:
  r = requests.get(
    telegram_url+'/getUpdates', 
    params={
      'offset': last_update
    }
  )
  response: GetUpdatesResponse = r.json()

  if len(response['result']) > 0:
    for update in response['result']:
      parse_response(update)
      last_update = update['update_id']+1

  sleep(1)