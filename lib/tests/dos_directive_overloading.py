"""Directive overloading tests."""
from lib.utils import graph_query

def directive_overloading(url, proxy, headers):
  """Check for directive overloading."""
  result = False

  q = 'query { __typename @aa@aa@aa@aa@aa@aa@aa@aa@aa@aa }'
  gql_response = graph_query(url, proxies=proxy, headers=headers, payload=q)

  try:
    if len(gql_response['errors']) == 10:
      result = True
  except:
    pass

  return result
