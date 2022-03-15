"""Batch tests."""
from lib.utils import graph_batch_query, get_error


def batch_query(url, proxy, headers):
  """Check for batch queries."""
  result = False

  gql_response = graph_batch_query(url, proxies=proxy, headers=headers, payload='query { __typename }')

  try:
      if len(gql_response) >= 10:
        result = True
  except:
    pass

  return result
