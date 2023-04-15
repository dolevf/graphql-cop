"""Collect trace mode details."""
from lib.utils import graph_query, curlify


def trace_mode(url, proxy, headers, debug_mode):
  """Get the trace mode."""
  res = {
    'result':False,
    'title':'Trace Mode',
    'description':'Tracing is Enabled',
    'impact':'Information Leakage - /' + url.rsplit('/', 1)[-1],
    'severity':'INFO',
    'color': 'green',
    'curl_verify':''
  }

  q = 'query cop { __typename }'

  try:
    if debug_mode:
      headers['X-GraphQL-Cop-Test'] = res['title']
    gql_response = graph_query(url, proxies=proxy, headers=headers, payload=q)
    res['curl_verify'] = curlify(gql_response)
    if gql_response.json()['errors'][0]['extensions']['tracing']:
      res['result'] = True
    elif '\'extensions\': {\'tracing\':' in str(gql_response.json()).lower():
      res['result'] = True
  except:
    pass

  return res
