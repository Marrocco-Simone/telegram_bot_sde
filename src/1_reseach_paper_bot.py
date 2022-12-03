from common.methods.parseUpdate import UpdateInfo
from common.methods.startServer import startServerPolling


def parse_response(update_info: UpdateInfo):
    # use this keyword to search the papers
    keyword = update_info['message']
    # send the messages to this chat
    chat_id = update_info['chat_id']

    # exercise 3:
    # use getResearchPaper() to retrieve the first 5 papers from the API
    # and send their abstracts back with sendTelegramMessage().
    # Remember to put your code inside a try-except block
    # and to send an error message to the user if something goes wrong.
    #
    # you can use this pre-made functions to search the papers and send the messages:
    # getResearchPapers(string keyword, int limit, int offset) <-- use pagination
    # sendTelegramMessage(chat_id, string message)



startServerPolling(parse_response)
