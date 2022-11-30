from time import time
from common.classes.classes import ResponseException
from common.methods.getResearchPapers import getResearchPapers
from common.methods.parseUpdate import UpdateInfo
from common.methods.sendTelegramMessage import sendTelegramMessage
from common.methods.startServer import startServerPolling
from common.methods.summarizeWithML import summarizeWithML

def parse_response(update_info: UpdateInfo):
  chat_id = update_info['chat_id']
  sender = update_info['sender']
  message = update_info['message']
  print(f'{sender} ({chat_id}) has sent: {message}')
  # 1 part - parrot bot ------------------------------------------

  sendTelegramMessage(chat_id, f'You wrote: {message}')

  # 2 part - get research papers --------------------------------
  
  # We retrieve the abstracts from Core AC API and we send to the user
  # their content in the form of Telegram messages.
  #'''
  core_ac_response = getResearchPapers(message)
  abstracts_text = ""
  try:
    for s in core_ac_response['results']:
      new_abstract = s['abstract']
      sendTelegramMessage(chat_id, new_abstract)
      abstracts_text += new_abstract
  except:
    sendTelegramMessage(chat_id, 'Error retrieving the abstracts')
    return
  #'''

  # 3 part - summarize with ML -----------------------------------
  # 3.1 Send a message to the user informing him that the summarization 
  # could take time
  #'''
  return_msg = f"Summarizing the paper Abstracts, this can take some time..."
  sendTelegramMessage(update_info['chat_id'], return_msg)
  #'''

  # 3.2 call summarizeWithML giving in input the abstracts text and
  # properly handle the ResponseException it could arise, sending a
  # message to the user informing him about the problem, then return
  #'''
  try:
    hugging_face_obj = summarizeWithML(abstracts_text)
    print('HuggingFace responded')
  except ResponseException:
    return_msg = f"Sorry, request failed at HuggingFace API. Reason: Model is loading, wait some time and retry"
    sendTelegramMessage(update_info['chat_id'], return_msg)
    return
  #'''

  # 3.3 Send a message to the user, containing the summarized text.
  # Remember to properly handle a possible exception, if that happen
  # you can access the error message by doing hugging_face_obj['error']
  # send a message informing the user.
  #'''
  try:
    return_msg = hugging_face_obj[0]['summary_text']
    sendTelegramMessage(update_info['chat_id'], return_msg)
  except:
    error_msg = hugging_face_obj['error']
    print(f"crashed hugging face api. Reason: {error_msg}")
    return_msg = f"Sorry, request failed at HuggingFace API. Reason: {error_msg}. Retry"
    sendTelegramMessage(update_info['chat_id'], return_msg)
    return
  #'''

startServerPolling(parse_response)