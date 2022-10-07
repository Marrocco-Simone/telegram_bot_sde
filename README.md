# Create your Bot
Go on Telegram and chat with [@BotFather](https://t.me/BotFather)

Follow his instructions and create a new Bot. More info in the [official docs](https://core.telegram.org/bots)

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

A simple server made with it is in the file _*auto_bot.py*_

The problem with this library is that we aren't using any Telegram API, so feel free to use this code just to test that our Bot is ready.

## Asking the endpoints
All queries to the Telegram Bot Api must be made by the url `https://api.telegram.org/bot<token>/METHOD_NAME`. The value to include in the request can be put either in the query params or in the body as _application/json_

### The method getUpdates
By using `getUpdates` as the *METHOD_NAME*, we can ask the server about the recent updates. They usually remain up to 24 hours, but we can delete them sooner by using the *offset* param. Every new update has an incremental _update\_id_ that we can use in the request: for example, using method GET and the query params, `https://api.telegram.org/bot<token>/getUpdates?offset={update_id}`. With this, we are going to get only the updates that have id equal or greater than it, and the previous ones are going to be deleted.

The response object is a JSON with a defined schema: you can find the full definition [here](https://core.telegram.org/bots/api#message), but in _classes.py_ you will find the schemas ready to use for your python file. This particular method is an array of *Update*, each one with an id and a *Message* containing the *text*, the *chat* and *from* whom the message came.

So what we want to do with this method is an infinite loop where each time we ask the url with the offset, parse the request and then update a counter variable, so that each time we request only the new messages. Of course, for performance it is advised to use a sleep at the end of the cycle, to avoid thousand of useless requests per seconds (at least in our little example). We will see later how to receive the data only when it's ready with web hooks.

You can see an example of such program in _getUpdates\_bot.py_, where it is also shown ho to send back simple messages

### The method sendMessage
The documentation may help you to understand all the possible methods. [Here](https://core.telegram.org/bots/api#sendmessage) the one for the method used to send a message.

This time this method requires two arguments (remember that you can pass them within the body in a POST request or in the query params of a GET request): the first one, _chat\_id_, is for identifying the chat; the second argument, _text_, is the message you want to send. The endpoint returns the *Message* object created from your request.