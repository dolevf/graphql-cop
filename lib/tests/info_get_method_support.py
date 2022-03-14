"""Collect all supported methods."""
from lib.utils import request_get


def get_method_support(url):
  """Get the supported methods."""
  result = False

  q = '{__typename}'
  
  response = request_get(url, params={'query':q})
  
  try:
    if response and response.json()['data']['__typename']:
      result = True
  except:
      pass
  
  return result
