from typing import Any, List, TypedDict
import datetime as dt

class WeatherStackRequest(TypedDict):
  type: str
  query: str
  language: str
  unit: str

class WeatherStackLocation(TypedDict):
    name: str
    country: str
    region: str
    lat: float
    lon: float
    timezone_id: str
    localtime: dt.datetime
    localtime_epoch: int
    utc_offset: float

class WeatherStackCurrent(TypedDict):
  observation_time: dt.datetime
  temperature: int
  weather_code: int
  weather_icons: List[str]
  weather_descriptions: List[str]
  wind_speed: int
  wind_degree: int
  wind_dir: str
  pressure: int
  precip: int
  humidity: int
  cloudcover: int
  feelslike: int
  uv_index: int
  visibility: int
  is_day: str

class WeatherStackResponse(TypedDict):
  request: WeatherStackRequest
  location: WeatherStackLocation  
  current: WeatherStackCurrent

class MapBoxFeatures(TypedDict):
  id: str
  type: str
  place_type: List[str]
  relevance: int
  properties: Any
  text: str
  place_name: str
  bbox: List[float]
  center: List[float]
  geometry: Any
  context: Any

class MapBoxResponse(TypedDict):
    type: str
    query: List[str]
    features: List[MapBoxFeatures]
    attribution: str
