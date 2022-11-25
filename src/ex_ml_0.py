# Machine Learning API
# Exercise 0

import requests
from common.classes.hugging_face_classes import HuggingFaceResponse
from dotenv import load_dotenv # retrieve tokens from .env file
import os

load_dotenv()
HUGGING_FACE_TOKEN = os.getenv('HUGGING_FACE_TOKEN')

# Define the url to call the API
hugging_face_url = 'https://api-inference.huggingface.co/models/google/bigbird-pegasus-large-pubmed'

# method to summarize some text
def summarizeWithML(text_to_summarize: str):
  '''summarize a text using an ml model from Hugging Face'''

  # 1 Do the POST request to he hugging face endpoint
  # hint: to do the request you can use requests package
  # https://requests.readthedocs.io/en/latest/user/quickstart/#make-a-request

  response = requests.post(
    hugging_face_url, 
    headers={
      "Authorization": f"Bearer {HUGGING_FACE_TOKEN}"
    }, 
    json=str({"text" : text_to_summarize})
  )

  # 2 Check if the response status code is 503, if so, print something 
  # and return. 
  # If hugging face is loading the model, it will return a
  # 503 error message, 

  if response.status_code == 503:
    print("error, model is loading, wait and try again")
    return HuggingFaceResponse

  # 3 Assign the json contained in the body of the response to a new 
  # huggingFaceResponse object
  # hint: name_of_variable: name_of_class = content_to_assign
  # hint: https://requests.readthedocs.io/en/latest/user/quickstart/#json-response-content

  hugging_face_obj: HuggingFaceResponse = response.json()

  # 4 Return a huggingFaceResponse object containing the response

  return hugging_face_obj

# 5 Call the function and print the result

print(summarizeWithML("Different services use different packet transmission techniques.In general, packets that must get through in the correct order, without loss, use TCP, whereas real time services where later packets are more important than older packets use UDP.For example, file transfer requires complete accuracy and so is normally done using TCP, and audio conferencing is frequently done via UDP, where momentary glitches may not be noticed.UDP lacks built-in network congestion avoidance and the protocols that use it must be extremely carefully designed to prevent network collapse.")[0]['summary_text'])