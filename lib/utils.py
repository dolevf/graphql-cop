import requests
#from config import HEADERS
from version import VERSION

requests.packages.urllib3.disable_warnings()

def get_error(resp):
  error = None
  try:
      error = resp['errors'][0]['message']
  except:
      pass
  return error

def graph_query(url, proxies, headers, operation='query', payload={}):
  try:
    response = requests.post(url,
                            headers=headers,
                            cookies=None,
                            verify=False,
                            allow_redirects=True,
                            timeout=60,
                            proxies=proxies,
                            json={operation:payload})
    return response.json()
  except:
    return {}

def graph_batch_query(url, proxies, headers, operation='query', payload={}, batch=10):
  try:
    batch_query = []
    
    for _ in range(0, batch+1):
      batch_query.append({operation:payload})
    
    response = requests.post(url,
                            headers=headers,
                            cookies=None,
                            verify=False,
                            allow_redirects=True,
                            timeout=5,
                            proxies=proxies,
                            json=batch_query)
    return response.json()
  except:
    return {}

def request_get(url, proxies, headers, params=None):
  try:
    response = requests.get(url,
                            params=params,
                            headers=headers,
                            cookies=None,
                            verify=False,
                            allow_redirects=True,
                            proxies=proxies,
                            timeout=5)
    return response
  except:
    return None

def is_graphql(url, proxies, headers):
  query = '''
    query {
      __typename
    }
  '''
  response = graph_query(url, proxies, headers, payload=query)
  if response.get('data', {}).get('__typename', '') in ('Query', 'QueryRoot', 'query_root'):
    return True
  elif response.get('errors') and (any('locations' in i for i in response['errors']) or (any('extensions' in i for i in response))):
    return True
  elif response.get('data'):
    return True
  else:
    return False

def draw_art():
  return '''
                GraphQL Cop {version}
           Security Auditor for GraphQL
             Dolev Farhi & Nick Aleks
  '''.format(version=VERSION)
