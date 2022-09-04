"""Collect all supported methods."""
from lib.utils import request, curlify


def get_method_support(url, proxies, headers):
  """Get the supported methods."""
  res = {
    'result':False,
    'title':'GET Method Query Support',
    'description':'GraphQL queries allowed using the GET method',
    'impact':'Possible Cross Site Request Forgery (CSRF) - /' + url.rsplit('/', 1)[-1],
    'severity':'MEDIUM',
    'curl_verify':''
  }

  q = 'query cop {__typename}'

  response = request(url, proxies=proxies, headers=headers, params={'query':q})
  res['curl_verify'] = curlify(response)

  try:
    if response and response.json()['data']['__typename']:
      res['result'] = True
  except:
      pass

  return res
