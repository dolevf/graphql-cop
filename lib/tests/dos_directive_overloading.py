"""Directive overloading tests."""
from lib.utils import graph_query, curlify


def directive_overloading(url, proxy, headers):
  """Check for directive overloading."""
  res = {
    'result':False,
    'title':'Directive Overloading',
    'description':'Multiple duplicated directives allowed in a query',
    'impact':'Denial of Service - /' + url.rsplit('/', 1)[-1],
    'severity':'HIGH',
    'curl_verify':''
  }

  q = 'query cop { __typename @aa@aa@aa@aa@aa@aa@aa@aa@aa@aa }'
  gql_response = graph_query(url, proxies=proxy, headers=headers, payload=q)
  res['curl_verify'] = curlify(gql_response)

  try:
    if len(gql_response.json()['errors']) == 10:
      res['result'] = True
  except:
    pass

  return res
