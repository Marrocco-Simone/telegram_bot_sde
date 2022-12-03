from typing import Callable, TypedDict

from common.classes.classes import Update


class UpdateInfo(TypedDict):
    chat_id: str
    sender: str
    message: str


def parseUpdate(update: Update, parseResponse: Callable[[UpdateInfo], None]):
    '''parse a single update by logging it, getting the important fields and calling parseResponse()'''

    chat_id = update['message']['chat']['id']
    sender = update['message']['chat']['username']
    if ('text' in update['message'].keys()):
        message = update['message']['text']
        print(f"{sender} says: {message}")

        update_info: UpdateInfo = {
            "chat_id": chat_id,
            "sender": sender,
            "message": message
        }
        parseResponse(update_info)
