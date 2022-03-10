"""Field duplication tests."""
from lib.utils import graph_query


def field_duplication(url):
  """Check for field duplication."""
  result = False

  duplicated_string = '__typename \n' * 500
  q = 'query { ' + duplicated_string + '} '
  gql_response = graph_query(url, payload=q)
  try:
    if gql_response['data']['__typename']:
      result = True
  except:
    pass
  
  return result
