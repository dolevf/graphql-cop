"""Alias overloading tests."""
from lib.utils import graph_query, curlify


def alias_overloading(url, proxy, headers):
  """Check for alias overloading."""
  res = {
    'result':False,
    'title':'Alias Overloading',
    'description':'Alias Overloading with 100+ aliases is allowed',
    'impact':'Denial of Service - /' + url.rsplit('/', 1)[-1],
    'severity':'HIGH',
    'curl_verify':''
  }
  aliases = ''

  for i in range(0, 101):
     aliases += 'alias{}:__typename \n'.format(i)

  gql_response = graph_query(url, proxies=proxy, headers=headers, payload='query cop { ' + aliases + ' }')

  res['curl_verify'] = curlify(gql_response)

  try:
    if gql_response.json()['data']['alias100']:
      res['result'] = True
  except:
    pass

  return res
