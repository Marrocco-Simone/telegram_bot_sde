from typing import List, TypedDict

class User(TypedDict): 
  # unique id of the user
  id: int
  # other data of the user
  is_bot: bool
  first_name: str
  last_name: str
  username: str
  language_code: str # en

class Chat(TypedDict):
  #  type of conversation: private, group, ...
  type: str
  #  same fields as USER
  id: int
  first_name: str
  last_name: str
  username: str

class Message(TypedDict(
    # this strange thing is like writing below a simple from: User
    # since from is a reserved word, we need to do this
    "Message",
    {'from': User},
  )):
  #  id for the new message
  message_id: int
  chat: Chat
  #  unix date
  date: int
  #  the text sent
  text: str

class Update(TypedDict):
  #  id for the new update
  update_id: int
  message: Message

# the complete response object
class GetUpdatesResponse(TypedDict):
  ok: bool
  result: List[Update]

class SendMessageResponse(TypedDict):
  ok: bool
  result: Message