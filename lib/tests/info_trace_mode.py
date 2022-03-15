"""Collect trace mode details."""
from lib.utils import graph_query, get_error


def trace_mode(url, proxy, headers):
  """Get the trace mode."""
  result = False

  q = 'query { __typename }'
  gql_response = graph_query(url, proxies=proxy, headers=headers, payload=q)

  try:
    if gql_response.get('errors', {}).get('extensions', {}).get('tracing'):
      result = True
    elif gql_response.get('errors', {}).get('extensions', {}).get('exception', None):
      result = True
    elif 'stacktrace' in str(gql_response).lower():
      result = True
  except:
    pass

  return result
