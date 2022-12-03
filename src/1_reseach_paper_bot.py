from common.methods.parseUpdate import UpdateInfo
from common.methods.startServer import startServerPolling


def parseResponse(update_info: UpdateInfo):
    sender = update_info['sender']
    message = update_info['message']
    # use this keyword to search the papers
    keyword = message
    # send the messages to this chat
    chat_id = update_info['chat_id']
    print(f"User {sender} sent {keyword} on chat {chat_id}")

    # exercise 3:
    # use getResearchPaper() to retrieve the first 5 papers from the API
    # and send their abstracts back with sendTelegramMessage().
    # Remember to put your code inside a try-except block
    # and to send an error message to the user if something goes wrong.
    #
    # you can use this pre-made functions to search the papers and send the messages:
    # getResearchPapers(string keyword, int limit, int offset) <-- use pagination
    # sendTelegramMessage(chat_id, string message)



startServerPolling(parseResponse)
