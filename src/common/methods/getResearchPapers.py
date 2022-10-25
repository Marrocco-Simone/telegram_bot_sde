import requests
from common.classes.core_ac_classes import CoreACSearchResponse

# retrieve tokens from .env file
from dotenv import load_dotenv
import os
load_dotenv()
CORE_AC_TOKEN = os.getenv('CORE_AC_TOKEN')

core_ac_url = 'https://api.core.ac.uk/v3/search/works/'

def getResearchPapers(keyword: str):
  '''function to get research papers from the Core Ac API from a keyword'''
  r = requests.get(
    core_ac_url, 
    params={
      'q': keyword,
      'limit': 5
    }, 
    headers = {"Authorization": f"Bearer {CORE_AC_TOKEN}"}
  )
  core_ac_response: CoreACSearchResponse = r.json()
  return core_ac_response