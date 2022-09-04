"""Field suggestions tests."""
from lib.utils import graph_query, get_error, curlify


def field_suggestions(url, proxy, headers):
  """Retrieve field suggestions."""
  res = {
    'result':False,
    'title':'Field Suggestions',
    'description':'Field Suggestions are Enabled',
    'impact':'Information Leakage - /' + url.rsplit('/', 1)[-1],
    'severity':'LOW',
    'curl_verify':''
  }

  q = 'query cop { __schema { directive } }'
  gql_response = graph_query(url, proxies=proxy, headers=headers, payload=q)
  res['curl_verify'] = curlify(gql_response)

  try:
    if 'Did you mean' in get_error(gql_response.json()):
      res['result'] = True
  except:
    pass

  return res
