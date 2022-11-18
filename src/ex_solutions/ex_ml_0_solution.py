# Machine Learning API
# Exercise 0 solution

import requests
# Import a TypedDict to ease the managing of the response
from common.classes.hugging_face_classes import HuggingFaceResponse
# retrieve tokens from .env file
from dotenv import load_dotenv 
import os

# Load dotenv variables
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


  # 2 Check if the response status code is 503, if so, print something 
  # and return. 
  # If hugging face is loading the model, it will return a
  # 503 error message, 
  
  
  # 3 Assign the json contained in the body of the response to a new 
  # huggingFaceResponse object
  # hint: name_of_variable: name_of_class = content_to_assign
  # hint: https://requests.readthedocs.io/en/latest/user/quickstart/#json-response-content

  # 4 Return a huggingFaceResponse object containing the response

# 5 Call the function and print the result