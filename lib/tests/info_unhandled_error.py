"""Collect trace mode details."""
from lib.utils import graph_query, curlify
from lib.tests.info_graphiql import detect_graphiql

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

  try:
    gql_response = graph_query(url, proxies=proxy, headers=headers, payload=q)
    res['curl_verify'] = curlify(gql_response)
    if gql_response.json()['errors'][0]['extensions']['exception']:
      res['result'] = True
    elif '\'extensions\': {\'exception\':' in str(gql_response.json()).lower():
      res['result'] = True
  except:
    pass

  if hasattr(detect_graphiql, 'GraphQLIDEpath'):
    url = detect_graphiql.GraphQLIDEpath
    try:
      gql_response = graph_query(url, proxies=proxy, headers=headers, payload=q)
      res['curl_verify'] = curlify(gql_response)
      if gql_response.json()['errors'][0]['extensions']['exception']:
        res['result'] = True
      elif '\'extensions\': {\'exception\':' in str(gql_response.json()).lower():
        res['result'] = True
    except:
      pass

  return res
