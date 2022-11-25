# Machine Learning API
# Exercise 0

import requests
from common.classes.classes import ResponseException
from common.classes.hugging_face_classes import HuggingFaceResponse
from dotenv import load_dotenv # retrieve tokens from .env file
import os

# Load dotenv file and get token value
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

  # 2 Check if the response status code is 503, if so, raise a 
  # ResponseException with a custom message
  # If hugging face is loading the model, it will return a
  # 503 error message
  # hint: use raise()
  
  if response.status_code == 503:
    raise(ResponseException("error, model is loading, wait and try again"))

  # 3 Assign the json contained in the body of the response to a new 
  # huggingFaceResponse object
  # hint: name_of_variable: name_of_class = content_to_assign
  # hint: https://requests.readthedocs.io/en/latest/user/quickstart/#json-response-content

  hugging_face_obj: HuggingFaceResponse = response.json()

  # 4 Return a huggingFaceResponse object containing the response

  return hugging_face_obj