import requests
from common.classes.hugging_face_classes import HuggingFaceResponse

# retrieve tokens from .env file
from dotenv import load_dotenv
import os
load_dotenv()
HUGGING_FACE_TOKEN = os.getenv('HUGGING_FACE_TOKEN')

huggin_face_url = 'https://api-inference.huggingface.co/models/google/bigbird-pegasus-large-pubmed'

def useMlModel(abstracts_text: str):
  '''summarize a text using an ml model from Hugging Face'''
  hugging_face_response = requests.post(
    huggin_face_url, 
    headers={
      "Authorization": f"Bearer {HUGGING_FACE_TOKEN}"
    }, 
    json=abstracts_text
  )
  hugging_face_obj: HuggingFaceResponse = hugging_face_response.json()
  return hugging_face_obj