"""Checks mutation support over on GET."""
from lib.utils import request, curlify


def get_based_mutation(url, proxies, headers):
  res = {
    'result':False,
    'title':'Mutation is allowed over GET (possible CSRF)',
    'description':'GraphQL mutations allowed using the GET method',
    'impact':'Possible Cross Site Request Forgery - /' + url.rsplit('/', 1)[-1],
    'severity':'MEDIUM',
    'color': 'yellow',
    'curl_verify':''
  }

  q = 'mutation cop {__typename}'
  headers['X-GraphQL-Cop-Test'] = res['title']
  response = request(url, proxies=proxies, headers=headers, params={'query':q})
  res['curl_verify'] = curlify(response)
  try:
    if response and response.json()['data']['__typename']:
        res['result'] = True
  except:
      pass

  return res
