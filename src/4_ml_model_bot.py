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
    if len(core_ac_response['results'])==0:
      #if no paper is found, tell user what happened
      sendTelegramMessage(update_info['chat_id'], 'CoreAC was not able to find any result for '+keyword)
      return
    else:
      #retrive abstract from CoreAc response
      for s in core_ac_response['results']:
        abstracts_text += f"{s['abstract']}\n"
  except:
    print(f"ERROR: {core_ac_response}")
    if('error' in core_ac_response.keys()):
      return_msg = keyword+': Error getting the research papers: '+core_ac_response['error']
    else: 
      return_msg = keyword+': Unknown error getting the research papers. Please retry later.'; 
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
