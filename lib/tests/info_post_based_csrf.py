"""Checks if queries are allowed over POST not in JSON."""
from lib.utils import request, curlify


def post_based_csrf(url, proxies, headers):
  res = {
    'result':False,
    'title':'POST based url-encoded query (possible CSRF)',
    'description':'GraphQL accepts non-JSON queries over POST',
    'impact':'Possible Cross Site Request Forgery',
    'severity':'MEDIUM',
    'curl_verify':''
  }

  q = 'query {__typename}'

  response = request(url, proxies=proxies, headers=headers, params={'query':q}, verb='POST')
  res['curl_verify'] = curlify(response)

  try:
    if response and response.json()['data']['__typename']:
        res['result'] = True
  except:
      pass

  return res
