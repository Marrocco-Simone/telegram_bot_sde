import json
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
  #print(r.headers)

  x_ratelimit_remaining = 2

  try:
    x_ratelimit_remaining = int(r.headers['X-RateLimit-Remaining'])
  except(KeyError):
    pass
  

  if(x_ratelimit_remaining>1):
    core_ac_response: CoreACSearchResponse = r.json()
    return core_ac_response
  else:
    return json.loads('{"error":"X-RateLimit-Remaining is at 0. Retry later at '+r.headers['X-RateLimit-Retry-After']+'"}')