"""Helper parts for graphql-cop."""
import os

import requests
from simplejson import JSONDecodeError
from version import VERSION

requests.packages.urllib3.disable_warnings()

def curlify(obj):
  req = obj.request
  command = "curl -X {method} -H {headers} -d '{data}' '{uri}'"
  method = req.method
  uri = req.url
  if req.body:
    try:
      data = req.body.decode('UTF-8')
    except:
      reqb = bytes(req.body, 'UTF-8')
      data = reqb.decode('UTF-8')
  else:
    data = ''
  headers = ['"{0}: {1}"'.format(k, v) for k, v in req.headers.items()]
  headers = " -H ".join(headers)
  return command.format(method=method, headers=headers, data=data, uri=uri)

def get_error(resp):
  """Collect the error."""
  error = None
  try:
      error = resp['errors'][0]['message']
  except:
      pass
  return error

def graph_query(url, proxies, headers, operation='query', payload={}, batch=False):
  """Perform a query."""
  if batch:
    data = []
    for _ in range(10):
      data.append({operation:payload})
  else:
    data = {operation:payload, "operationName":"cop"}
  try:
    response = requests.post(url,
                            headers=headers,
                            cookies=None,
                            verify=False,
                            allow_redirects=True,
                            timeout=60,
                            proxies=proxies,
                            json=data)
    return response
  except Exception:
    return {}


def request(url, proxies, headers, params=None, data=None, verb='GET'):
  """Perform requests."""
  try:
    response = requests.request(verb,
                            url=url,
                            params=params,
                            headers=headers,
                            cookies=None,
                            verify=False,
                            allow_redirects=True,
                            proxies=proxies,
                            timeout=20,
                            data=data)
    return response
  except:
    return None



def is_graphql(url, proxies, headers, debug_mode):
  """Check if the URL provides a GraphQL interface."""
  if debug_mode:
    headers['X-GraphQL-Cop-Test'] = 'Looking for GraphQL Interface'
  query = '''
    query cop {
      __typename
    }
  '''
  response = graph_query(url, proxies, headers, payload=query)

  try:
    response.json()
  except AttributeError:
    return False
  except JSONDecodeError:
    return False

  if 'data' in response.json() and response.json()['data'] != None:
    if response.json()['data']['__typename'] in ('Query', 'QueryRoot', 'query_root', 'Root'):
      return True
  elif response.json().get('errors') and (any('locations' in i for i in response.json()['errors']) or (any('extensions' in i for i in response.json()))):
    return True
  elif response.json().get('data'):
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


def read_custom_wordlist(location):
  wordlists = set()
  if os.path.exists(location):
    f = open(location, 'r').read()
    for line in f.splitlines():
      if not line.startswith('/'):
        line = '/' + line

      wordlists.add(line)
  else:
    print('Could not find wordlist file: {}'.format(location))
  return wordlists