import requests
from common.methods.parseUpdate import UpdateInfo
from common.classes.core_ac_classes import CoreACSearchResponse

core_ac_url = 'https://api.core.ac.uk/v3/search/works/'

def getResearchPapers(update_info: UpdateInfo, CORE_AC_TOKEN: str):
  r = requests.get(
    core_ac_url, 
    params={
      'q': update_info["message"],
      'limit': 5
    }, 
    headers = {"Authorization": f"Bearer {CORE_AC_TOKEN}"}
  )
  core_ac_response: CoreACSearchResponse = r.json()
  return core_ac_response