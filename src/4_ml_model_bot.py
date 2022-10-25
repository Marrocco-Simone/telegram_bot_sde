from time import time
from common.methods.getResearchPapers import getResearchPapers
from common.methods.parseUpdate import UpdateInfo
from common.methods.sendTelegramMessage import sendTelegramMessage
from common.methods.startServer import startServerPolling
from common.methods.summarizeWithML import summarizeWithML

def parse_response(update_info: UpdateInfo):
  start = time()
  sendTelegramMessage(update_info['chat_id'], "Elaborating request...")

  keyword = update_info['message']
  core_ac_response = getResearchPapers(keyword)
  
  abstracts_text = ""
  try:
    for s in core_ac_response['results']:
      abstracts_text += f"{s['abstract']}\n"
  except:
    error_msg = core_ac_response["message"]
    print(f'crashed core ac api. Reason: {error_msg}')
    return_msg = f'Sorry, request failed at CoreAc API. Reason: {error_msg}. Retry'
    sendTelegramMessage(update_info['chat_id'], return_msg)
    return

  core_ac_log = f'CoreAc responded with {len(core_ac_response["results"])} results, out of {core_ac_response["totalHits"]}'
  sendTelegramMessage(update_info['chat_id'], core_ac_log)
  print(core_ac_log)
  print(f"lenght of the abstract composition: {len(abstracts_text)}")

  hugging_face_obj = summarizeWithML(abstracts_text)
  print('HuggingFace responded')

  try:
    return_msg = hugging_face_obj[0]['summary_text']
    sendTelegramMessage(update_info['chat_id'], return_msg)
  except:
    error_msg = hugging_face_obj['error']
    print(f"crashed hugging face api. Reason: {error_msg}")
    return_msg = f"Sorry, request failed at HuggingFace API. Reason: {error_msg}. Retry"
    sendTelegramMessage(update_info['chat_id'], return_msg)
    return

  end = time()
  print(f"request served in {end-start} s")

startServerPolling(parse_response)
