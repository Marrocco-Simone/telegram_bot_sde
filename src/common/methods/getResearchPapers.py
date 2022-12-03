import json
import requests
from common.classes.core_ac_classes import CoreACSearchResponse
from common.classes.core_ac_classes import CoreACException

# retrieve tokens from .env file
from dotenv import load_dotenv
import os
load_dotenv()
CORE_AC_TOKEN = os.getenv('CORE_AC_TOKEN')

core_ac_url = 'https://api.core.ac.uk/v3/search/works/'

def getResearchPapers(keyword: str,limit: int=5, offset: int=0):
  '''function to get research papers from the Core Ac API from a keyword'''
  # 1. Get the papers
  # use core AC API to retrieve 5 papers from the first result
  # using the keyword as query
  r = requests.get(
    core_ac_url, 
    params={
      'q': keyword,
      'limit': limit,
      'offset': offset
    }, 
    headers = {"Authorization": f"Bearer {CORE_AC_TOKEN}"}
  )


  # 2. check the headers: Core AC API limits the number of
  # requests that you can make, so we have to check if we
  # have breached this limit everytime we request something 
  # from the API to make sure we got a response with the right 
  # content. The response header 'X-RateLimit-Remaining' tells
  # us how many requests we have left.

  x_ratelimit_remaining = 2

  try:
    x_ratelimit_remaining = int(r.headers['X-RateLimit-Remaining'])
  except(KeyError):
    pass
  
  # 3. If the response is ok, we can parse the json and return,
  # otherwise we return an error object explaining the problem

  if(x_ratelimit_remaining>1):
    core_ac_response: CoreACSearchResponse = r.json()
    return core_ac_response
  else:
    raise CoreACException('X-RateLimit-Remaining is at 0. Retry later at '+r.headers['X-RateLimit-Retry-After'])