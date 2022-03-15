"""Collect all supported methods."""
from lib.utils import request_get


def get_method_support(url, proxies, headers):
  """Get the supported methods."""
  result = False

  q = '{__typename}'

  response = request_get(url, proxies=proxies, headers=headers, params={'query':q})

  try:
    if response and response.json()['data']['__typename']:
      result = True
  except:
      pass

  return result
