from common.methods.getResearchPapers import getResearchPapers
from common.methods.parseUpdate import UpdateInfo
from common.methods.sendTelegramMessage import sendTelegramMessage
from common.methods.startServer import startServerPolling

def parse_response(update_info: UpdateInfo):
  core_ac_response = getResearchPapers(update_info)

  try:
    # send a message for each abstract received
    for s in core_ac_response['results']:
      return_msg = s['abstract']
      sendTelegramMessage(update_info['chat_id'], return_msg)
  except:
    print(f"ERROR: {core_ac_response}")
    return_msg = 'Error getting the research papers'
    sendTelegramMessage(update_info['chat_id'], return_msg)

startServerPolling(parse_response)
