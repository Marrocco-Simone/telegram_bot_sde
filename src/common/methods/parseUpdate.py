from typing import TypedDict
from common.classes.classes import Update

class UpdateInfo(TypedDict):
  chat_id: str
  sender: str
  message: str

def parseUpdate(update: Update) -> UpdateInfo:
  chat_id = update['message']['chat']['id']
  sender = update['message']['chat']['username']
  message = update['message']['text']
  print(f"\n{sender} says: {message}")
  update_info: UpdateInfo = { 
    "chat_id": chat_id, 
    "sender": sender, 
    "message": message 
  }
  return update_info