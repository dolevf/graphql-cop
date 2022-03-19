"""Collect GraphiQL details."""
from urllib.parse import urlparse
from lib.utils import request_get, curlify


def detect_graphiql(url, proxy, headers):
  """Get GraphiQL."""
  res = {
    'result':False,
    'title':'GraphQL IDE',
    'description':'GraphiQL Explorer/Playground Enabled',
    'impact':'Information Leakage',
    'severity':'LOW',
    'curl_verify':''
  }

  heuristics = ('graphiql.min.css', 'GraphQL Playground', 'GraphiQL', 'graphql-playground')
  endpoints = ['/graphiql', '/playground', '/console', '/graphql']

  parsed = urlparse(url)
  url = '{}://{}'.format(parsed.scheme, parsed.netloc)

  for endpoint in endpoints:
    response = request_get(url + endpoint, proxies=proxy, headers=headers)
    res['curl_verify'] = curlify(response)
    try:
      if response and any(word in response.text for word in heuristics):
        res['result'] = True
        break
    except:
      pass

  return res
