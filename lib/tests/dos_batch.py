"""Batch tests."""
from lib.utils import graph_batch_query, get_error


def batch_query(url):
  """Check for batch queries."""
  result = False
  
  gql_response = graph_batch_query(url, payload='query { __typename }')

  try:
      if len(gql_response) >= 10:
        result = True
  except:
    pass
  
  return result
