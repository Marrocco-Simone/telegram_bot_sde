from common.methods.getResearchPapers import getResearchPapers
from common.methods.parseUpdate import UpdateInfo
from common.methods.sendTelegramMessage import sendTelegramMessage
from common.methods.startServer import startServerPolling

def parse_response(update_info: UpdateInfo):
  keyword = update_info['message']
  core_ac_response = getResearchPapers(keyword)
  #print(core_ac_response)
  try:
    if len(core_ac_response['results'])==0:
      sendTelegramMessage(update_info['chat_id'], 'CoreAC was not able to find any result for '+keyword)
    else:
      # send a message for each abstract received
      for s in core_ac_response['results']:
        return_msg = s['abstract']
        sendTelegramMessage(update_info['chat_id'], return_msg)
  except:
    print(f"ERROR: {core_ac_response}")
    if('error' in core_ac_response.keys()):
      return_msg = keyword+': Error getting the research papers: '+core_ac_response['error']
    else: 
      return_msg = keyword+': Unknown error getting the research papers. Please retry later.'; 
    sendTelegramMessage(update_info['chat_id'], return_msg)

startServerPolling(parse_response)
