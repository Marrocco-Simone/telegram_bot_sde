from common.classes.classes import SendMessageResponse
from common.methods.parseUpdate import UpdateInfo
from common.methods.sendTelegramMessage import sendTelegramMessage
from common.methods.startServer import startServerPolling


def parse_response(update_info: UpdateInfo):
    chat_id = update_info["chat_id"]
    sender = update_info["sender"]
    message = update_info["message"]
    print(f"User {sender} sent {message} on chat {chat_id}")
    
    # send here the response
    sendTelegramMessage(chat_id, f"Hi {sender}, you sent {message}")
    ########################


startServerPolling(parse_response)
