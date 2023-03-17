"""Collect GraphiQL details."""
from lib.utils import request, curlify

def detect_graphiql(url, proxy, headers):
  """Get GraphiQL."""
  res = {
    'result':False,
    'title':'GraphQL IDE',
    'description':'GraphiQL Explorer/Playground Enabled',
    'impact':'Information Leakage - /' + url.rsplit('/', 1)[-1],
    'severity':'LOW',
    'color': 'blue',
    'curl_verify':''
  }

  heuristics = ('graphiql.min.css', 'GraphQL Playground', 'GraphiQL', 'graphql-playground')

  if "Accept" in headers.keys():
    backup_accept_header=headers["Accept"]
  headers["Accept"]= "text/html"

  response = request(url, proxies=proxy, headers=headers)
  res['curl_verify'] = curlify(response)
  try:
    if response and any(word in response.text for word in heuristics):
      res['result'] = True
  except:
      pass

  del headers["Accept"]
  if 'backup_accept_header' in locals():
    headers["Accept"]=backup_accept_header

  return res
