# MachineLearning
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
def summarizeWithML(abstracts_text: str):
  '''summarize a text using an ml model from Hugging Face'''
  hugging_face_response = requests.post(
    hugging_face_url, 
    headers={
      "Authorization": f"Bearer {HUGGING_FACE_TOKEN}"
    }, 
    json=str({"text" : abstracts_text})
  )
  print(hugging_face_response)
  hugging_face_obj: HuggingFaceResponse = hugging_face_response.json()

  return hugging_face_obj

print(summarizeWithML("Different services use different packet transmission techniques.In general, packets that must get through in the correct order, without loss, use TCP, whereas real time services where later packets are more important than older packets use UDP.For example, file transfer requires complete accuracy and so is normally done using TCP, and audio conferencing is frequently done via UDP, where momentary glitches may not be noticed.UDP lacks built-in network congestion avoidance and the protocols that use it must be extremely carefully designed to prevent network collapse."))