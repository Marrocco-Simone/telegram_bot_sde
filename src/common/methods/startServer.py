from time import sleep
from typing import Callable
from common.methods.getTelegramUpdates import getTelegramUpdates
from common.methods.parseUpdate import UpdateInfo, parseUpdate

def startServerPolling(parse_response: Callable[[UpdateInfo], None]):
  '''start the telegram listener with polling (aka constantly asking'''
  print("Server online. Waiting...")
  # id of the last parsed message
  last_update = 0
  while True:
    response = getTelegramUpdates(last_update)

    if len(response['result']) > 0:
      for update in response['result']:
        parseUpdate(update, parse_response)
        last_update = update['update_id']+1

    sleep(1)
