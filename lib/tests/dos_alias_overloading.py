"""Alias overloading tests."""
from lib.utils import graph_query, get_error


def alias_overloading(url, proxy, headers):
  """Check for alias overloading."""
  result = False
  aliases = ''

  for i in range(0, 101):
     aliases += 'alias{}:__typename \n'.format(i)

  gql_response = graph_query(url, proxies=proxy, headers=headers, payload='query { ' + aliases + ' }')

  try:
    if gql_response['data']['alias100']:
      result = True
  except:
    pass
  
  return result
