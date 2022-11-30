from time import sleep
from typing import Callable
from common.methods.getTelegramUpdates import getTelegramUpdates
from common.methods.parseUpdate import UpdateInfo, parseUpdate
import threading

def startServerPolling(parse_response: Callable[[UpdateInfo], None]):
  '''start the telegram listener with polling'''

  print("Server online. Waiting...")
  # id of the last parsed update
  last_update = 0

  # The server will do polling: once every second
  # a new request will be generated to get the updates
  # from Telegram. The server will run for an indefinite 
  # amount of time and can only be stopped using an
  # interrupting signal (exaple: CTRL + C)
  while True:
    response = getTelegramUpdates(last_update)

    if len(response['result']) > 0:
      for update in response['result']:
        # without threading
        # parseUpdate(update, parse_response)
        
        # with threading
        new_thread = threading.Thread(target=parseUpdate, args=(update, parse_response))
        new_thread.start()
        
        last_update = update['update_id']+1

    sleep(1)
