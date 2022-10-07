from telegram.ext import Updater, CommandHandler

from dotenv import load_dotenv
import os
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

def start(update, context):
  context.bot.send_message(chat_id=update.effective_chat.id, text='Hi, welcome to the newest bot!\nTry me with the command /hello_world')

def hello_there(update, context):
  context.bot.send_message(chat_id=update.effective_chat.id, text='Hello There')

def main():
  print("We're online!")
  updater = Updater(token=BOT_TOKEN, use_context=True)
  dispatcher = updater.dispatcher
  hello_there_handler = CommandHandler("hello_there", hello_there)
  start_handler = CommandHandler("start", start)

  dispatcher.add_handler(hello_there_handler)
  dispatcher.add_handler(start_handler)

  updater.start_polling()

if __name__ == '__main__':
  main()