# Create your Bot
Go on Telegram and chat with [@BotFather](https://t.me/BotFather)

Follow his instructions and create a new Bot. More info in the [official docs](https://core.telegram.org/bots)

Duplicate the _.env.example_ file and rename it as _.env_. Save the token inside this file as the **BOT_TOKEN** variable

> The token is used to respond to the user requests. Keep it secret 🤫

> To use the _.env_ file inside a python program, install it with `pip install python-dotenv`. Then, inside the program, write at the start: 
> ```
>from dotenv import load_dotenv
>import os
>load_dotenv()
>BOT_TOKEN = os.getenv("BOT_TOKEN")
>```
>The token will be available in the **BOT_TOKEN** variable.
>
>For our bot, our .env file will need three tokens: **BOT_TOKEN**, **CORE_AC_TOKEN**, and ***HUGGING_FACE_TOKEN**. Usually in every project that uses a .env file is present a _.env.example_ file with shows the model the env file should follow, included this one

# Create the Bot Server

## The easy way: python-telegram-bot

We could use an easy-to-use python library to create our server. To install it, use `pip install python-telegram-bot`.

A simple server made with it is in the file _**auto_bot.py**_

The problem with this library is that we aren't using any Telegram API, so feel free to use this code just to test that our Bot is ready.

## Asking the endpoints
All queries to the Telegram Bot Api must be made by the url `https://api.telegram.org/bot<token>/METHOD_NAME`. The value to include in the request can be put either in the query params or in the body as _application/json_

### Disclaimer: WebHooks
In the next part we are going to see how to create our Telegram server by constantly asking for updates. There is a more efficient way to do that by using webhooks: you send an url to the Telegram API and when an update is ready it will be automatically be sent to you.

Unfortunately, to give an url from our personal machine is no easy task: most wifi networks today use NAT and we would need to set up port forwarding and other things. So for this tutorial we will use this more inefficient but easier version: if you want to actually deploy a Telegram server be sure to change the method. More on this [here](https://core.telegram.org/bots/api#setwebhook) and [here](https://core.telegram.org/bots/webhooks), while for port forwarding [here](https://portforward.com/)

### The method getUpdates
By using `getUpdates` as the **METHOD_NAME**, we can ask the server about the recent updates. They usually remain up to 24 hours, but we can delete them sooner by using the **offset** param. Every new update has an incremental _update\_id_ that we can use in the request: for example, using method GET and the query params, `https://api.telegram.org/bot<token>/getUpdates?offset={update_id}`. With this, we are going to get only the updates that have id equal or greater than it, and the previous ones are going to be deleted.

The response object is a JSON with a defined schema: you can find the full definition [here](https://core.telegram.org/bots/api#message), but in _classes.py_ you will find the schemas ready to use for your python file. This particular method is an array of **Update**, each one with an id and a **Message** containing the **text**, the **chat** and **from** whom the message came.

So what we want to do with this method is an infinite loop where each time we ask the url with the offset, parse the request and then update a counter variable, so that each time we request only the new messages. Of course, for performance it is advised to use a sleep at the end of the cycle, to avoid thousand of useless requests per seconds (at least in our little example).

An example of this method can be found on *getTelegramUpdates.py*. The polling part is shown in *startServer.py* on the method *startServerWithPolling()*

> Processing a request may take time, and we don't want to block the server for each one of them. A good idea is to delegate the request parsing to a new thread. We can do that with the *threading* library, where we can create a new thread with `new_thread = threading.Thread(target=functionToThread, args=(arg1, arg2, ecc))` and start it with `new_thread.start()`. The new thread will now be executed as being a different programm, and our main server can delegate the incoming requested to different threads

### The method sendMessage
The documentation may help you to understand all the possible methods. [Here](https://core.telegram.org/bots/api#sendmessage) the one for the method used to send a message.

This time this method requires two arguments (remember that you can pass them within the body in a POST request or in the query params of a GET request): the first one, _chat\_id_, is for identifying the chat; the second argument, _text_, is the message you want to send. The endpoint returns the **Message** object created from your request.

An example of this method can be found on *sendTelegramMessage.py*.

### Parsing the user message
Now that we get the user message and can send back a response, it is time to set up some commands. In Telegram, commands are the first word of a message that starts with a **/**

So, we need first to parse the user message to see if it starts with this character, then we need to understand the word written after it. Then, we need various conditions to execute a specific action with each different command.

In _2\_commands\_and\_db\_bot.py_, you can see in **execute_command()** an example of this.

#### Easter egg: the method sendDice
You can send a dice to the user with the method sendDice, that requires only the _chat\_id_ param. This dice is an animated emoji: try it on Telegram!

An example of this method can be found on *sendDice.py*.

## Core Ac API

The Core Ac Api is useful to get research papers based on a keyword. The specific API we're going to use is described [here](https://api.core.ac.uk/docs/v3#tag/Search).

The endpoint is *https://api.core.ac.uk/v3/search/works/?q=(keyword)&limit=(N)*, where N is the number of results we want to show. 

Being an external service, we need an access token. You can get your by entering your email [here](https://core.ac.uk/services/api#form)

> You could also use a temporary mail, like https://10minutemail.com/

A function used to retrieve data from this API is found on *getResearchPapers.py*

## Hugging Face API

To get the Hugging Face Token, you need first to create an account. Then, go on Settings > Access Tokens and create a new token with role READ.

Every model has an API specification. You can find it in the *Deploy* button on the right, then *Inference API*. Below the computed text, you can also find the small *JSON Output* button to show the returned JSON.

The particular model we're going to use is *https://huggingface.co/google/bigbird-pegasus-large-pubmed*. You can find an example of a function that uses it in *summarizeWithML.py*