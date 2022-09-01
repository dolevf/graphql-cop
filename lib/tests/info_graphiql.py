"""Collect GraphiQL details."""
from urllib.parse import urlparse
from lib.utils import request, curlify

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
  endpoints = ['graphiql', 'playground', 'console', 'graphql']

  parsed = urlparse(url)
  if "Accept" in headers.keys():
    backup_accept_header=headers["Accept"]
  headers["Accept"]= "text/html"

  truepath = ""
  pathlist = parsed.path.split('/')
  for p in range(0, len(pathlist)):
    truepath += pathlist[p] + '/'
    url = '{}://{}{}'.format(parsed.scheme, parsed.netloc, truepath)
    for endpoint in endpoints:
      response = request(url + endpoint, proxies=proxy, headers=headers)
      res['curl_verify'] = curlify(response)
      try:
        if response and any(word in response.text for word in heuristics):
          detect_graphiql.GraphQLIDEpath = url + endpoint
          res['result'] = True
          break
      except:
        pass

  del headers["Accept"]
  if 'backup_accept_header' in locals():
    headers["Accept"]=backup_accept_header

  return res
