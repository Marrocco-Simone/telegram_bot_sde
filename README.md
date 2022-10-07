# Create your Bot
Go on Telegram and chat with [@BotFather](https://t.me/BotFather)

Follow his instructions and create a new Bot. 

Duplicate the _.env.example_ file and rename it as _.env_. Save the token inside this file as the *BOT_TOKEN* variable

> The token is used to respond to the user requests. Keep it secret 🤫

> To use the _.env_ file inside a python program, install it with `pip install python-dotenv`. Then, inside the program, write at the start: 
> ```
>from dotenv import load_dotenv
>import os
>load_dotenv()
>BOT_TOKEN = os.getenv("BOT_TOKEN")
>```
>The token will be available in the *BOT_TOKEN* variable

# Create the Bot Server

## The easy way: python-telegram-bot

We could use an easy-to-use python library to create our server. To install it, use `pip install python-telegram-bot`.

After that, here is a simple server:
```
from telegram.ext import Updater, CommandHandler

#function called for the start command
def start(update, context):
  #text to send
  text='Hi, welcome to the newest bot!\nTry me with the command /hello_world'
  #send the message as response
  context.bot.send_message(chat_id=update.effective_chat.id, text=text)

#function called for the hello_there command
def hello_there(update, context):
  #text to send
  text='Hello There'
  #send the message as response
  context.bot.send_message(chat_id=update.effective_chat.id, text=text)

def main():
  #log that the server is ready
  print("We're online!")

  #tell the Telegram server that our programm is ready to receive requests
  #identified by the BOT_TOKEN
  updater = Updater(token=BOT_TOKEN, use_context=True)
  dispatcher = updater.dispatcher

  #create command handlers: 
  # first param is the command
  # second param is the function to execute
  start_handler = CommandHandler("start", start)
  hello_there_handler = CommandHandler("hello_there", hello_there)

  #add the handlers to the dispatcher
  dispatcher.add_handler(hello_there_handler)
  dispatcher.add_handler(start_handler)

  #wait for updates
  updater.start_polling()

if __name__ == '__main__':
  main()
```
The problem with this library is that we aren't using any Telegram API, so feel free to use this code just to test that our Bot is ready.