import requests
from config import HEADERS
from version import VERSION

requests.packages.urllib3.disable_warnings()

def get_error(resp):
  error = None
  try:
      error = resp['errors'][0]['message']
  except:
      pass
  return error

def graph_query(url, operation='query', payload={}):
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

def severity_conversion(n):
  sevmap = {0:'Info', 1:'Low', 2:'Medium', 3:'High', 4:'Critical'}
  return sevmap[n].upper()


def draw_art():
  return '''
                GraphQL Cop {version}
           Security Auditor for GraphQL
         Dolev Farhi <dolev@lethalbit.com>
  '''.format(version=VERSION)