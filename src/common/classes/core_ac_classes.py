from typing import Any, List, TypedDict
import datetime as dt

class CoreACWork(TypedDict):
  accepted_date: dt.datetime
  authors: List[str]
  contributors: List[str]
  created_date: dt.datetime
  data_provider: List[str]
  deposited_date: dt.datetime
  abstract: str
  document_type: str
  doi: str
  oai: str
  download_url: str
  full_text: str
  id: int
  identifiers: List[Any]
  title: str
  language: Any
  published_date: dt.datetime
  publisher: Any
  references: List[Any]
  source_fulltext_urls: List[str]
  updated_date: dt.datetime
  year_published: str
  links: List[str]
  tags: List[str]
  fulltext_status: str
  subjects: List[str]
  deleted: str
  journals: str
  repositories: List[Any]
  repository_document: Any
  urls: List[str]
  disabled: int
  last_update: dt.datetime

class CoreACSearchResponse(TypedDict):
  totalHits: int
  limit: int
  offset: int
  scrollId: str
  results: List[CoreACWork]
  tooks: List[str]
  esTook: int

class CoreACException(Exception):
  def __init__(self, message):            
    # Call the base class constructor with the parameters it needs
    super().__init__(message)