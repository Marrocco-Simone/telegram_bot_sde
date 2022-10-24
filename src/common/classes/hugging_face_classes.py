from typing import List, TypedDict

class HuggingFaceSummary(TypedDict):
  summary_text: str

HuggingFaceResponse = List[HuggingFaceSummary]