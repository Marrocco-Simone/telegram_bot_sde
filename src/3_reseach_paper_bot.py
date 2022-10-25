from common.methods.getResearchPapers import getResearchPapers
from common.methods.parseUpdate import UpdateInfo
from common.methods.sendTelegramMessage import sendTelegramMessage
from common.methods.startServer import startServerPolling

def parse_response(update_info: UpdateInfo):
  core_ac_response = getResearchPapers(update_info)

  try:
    # send a message for each abstract received
    for s in core_ac_response['results']:
      sendTelegramMessage(update_info['chat_id'], s['abstract'])
  except:
    print(f"ERROR: {core_ac_response}")
    sendTelegramMessage(update_info['chat_id'], 'Error getting the research papers')

startServerPolling(parse_response)
