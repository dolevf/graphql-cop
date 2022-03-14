"""Helper parts for graphql-cop."""
import requests
from config import HEADERS
from version import VERSION

requests.packages.urllib3.disable_warnings()

def get_error(resp):
  """Collect the error."""
  error = None
  try:
      error = resp['errors'][0]['message']
  except:
      pass
  return error


def graph_query(url, operation='query', payload={}):
  """Perform a query."""
  try:
    response = requests.post(url,
                            headers=HEADERS,
                            cookies=None,
                            verify=False,
                            allow_redirects=True,
                            timeout=60,
                            json={operation:payload})
    return response.json()
  except:
    return {}


def graph_batch_query(url, operation='query', payload={}, batch=10):
  """Perform a batch query."""
  try:
    batch_query = []
    
    for _ in range(0, batch+1):
      batch_query.append({operation:payload})
    
    response = requests.post(url,
                            headers={'User-Agent':'graphql-cop'},
                            cookies=None,
                            verify=False,
                            allow_redirects=True,
                            timeout=5,
                            json=batch_query)
    return response.json()
  except:
    return {}


def request_get(url, params=None):
  """Perform requests."""
  try:
    response = requests.get(url,
                            params=params,
                            headers={'User-Agent':'graphql-cop'},
                            cookies=None,
                            verify=False,
                            allow_redirects=True,
                            timeout=5)
    return response
  except:
    return None


def is_graphql(url):
  """Check if the URL provides a GraphQL interface."""
  query = '''
    query {
      __typename
    }
  '''
  response = graph_query(url, payload=query)
  if response.get('data', {}).get('__typename', '') in ('Query', 'QueryRoot', 'query_root'):
    return True
  elif response.get('errors') and (any('locations' in i for i in response['errors']) or (any('extensions' in i for i in response))):
    return True
  elif response.get('data'):
    return True
  else:
    return False

def draw_art():
  """Create banner."""
  return '''
                GraphQL Cop {version}
           Security Auditor for GraphQL
             Dolev Farhi & Nick Aleks
  '''.format(version=VERSION)
