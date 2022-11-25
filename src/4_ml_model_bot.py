from time import time
from common.classes.classes import ResponseException
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

  # Send a message to the user informing him that the summarization could take time
  return_msg = f"Summarizing the paper Abstracts, this can take some time..."
  sendTelegramMessage(update_info['chat_id'], return_msg)

  # call summarizeWithML giving in input the abstracts text and
  # properly handle the ResponseException it could arise, sending a
  # message to the user informing him about the problem, then return
  try:
    hugging_face_obj = summarizeWithML(abstracts_text)
    print('HuggingFace responded')
  except ResponseException:
    return_msg = f"Sorry, request failed at HuggingFace API. Reason: Model is loading, wait some time and retry"
    sendTelegramMessage(update_info['chat_id'], return_msg)
    return

  # Send a message to the user, containing the summarized text.
  # Remember to properly handle a possible exception, if that happen
  # you can access the error message by doing hugging_face_obj['error']
  # send a message informing the user.
  # hint: you can access the summarized text by doing
  # hugging_face_obj[0]['summary_text']

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
