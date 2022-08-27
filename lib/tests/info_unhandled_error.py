"""Collect trace mode details."""
from lib.utils import graph_query, curlify


def unhandled_error_detection(url, proxy, headers):
  """Get the trace mode."""
  res = {
    'result':False,
    'title':'Unhandled Errors Detection',
    'description':'Exception errors are not handled',
    'impact':'Information Leakage',
    'severity':'INFO',
    'curl_verify':''
  }

  q = 'qwerty cop { abc }'
  gql_response = graph_query(url, proxies=proxy, headers=headers, payload=q)
  res['curl_verify'] = curlify(gql_response)

  try:
    if gql_response.json()['errors'][0]['extensions']['exception']:
      res['result'] = True
    elif 'exception' in str(gql_response.json()).lower():
      res['result'] = True
  except:
    pass

  return res
