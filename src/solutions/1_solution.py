from common.methods.getResearchPapers import getResearchPapers
from common.methods.parseUpdate import UpdateInfo
from common.methods.sendTelegramMessage import sendTelegramMessage
from common.methods.startServer import startServerPolling


def parse_response(update_info: UpdateInfo):
    keyword = update_info['message']
    chat_id = update_info['chat_id']

    # solution is:
    try:
        response = getResearchPapers(keyword)
        if len(response['results']) == 0:
            sendTelegramMessage(chat_id, 'CoreAC was not able to find any result for ' + keyword)
        else:
            for paper in response['results']:
                return_msg = paper['abstract']
                sendTelegramMessage(chat_id, return_msg)
    except:
        return_msg = 'Error getting the research papers. Please retry later.';
        sendTelegramMessage(chat_id, return_msg)


startServerPolling(parse_response)
