from common.classes.classes import SendMessageResponse
from common.methods.parseUpdate import UpdateInfo
from common.methods.sendTelegramMessage import sendTelegramMessage
from common.methods.startServer import startServerPolling


def parse_response(update_info: UpdateInfo):
    return_msg = f'Hi {update_info["sender"]}, you told me: {update_info["message"]}'
    r = sendTelegramMessage(update_info['chat_id'], return_msg)

    # analyze the return object from the sendMessage telegram method
    response: SendMessageResponse = r.json()
    msg_sent = response['result']['text']
    recipient = response['result']['chat']['username']
    print('you sent back to ' + recipient + ': {' + msg_sent + '}')


startServerPolling(parse_response)
