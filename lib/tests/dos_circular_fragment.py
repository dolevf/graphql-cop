"""Circular Fragment tests."""
from lib.utils import graph_query, curlify


def circular_fragment(url, proxy, headers):
  """Check for circular fragment."""
  res = {
    'result':False,
    'title':'Circular Fragment',
    'description':'Circular Fragment allowed in Query',
    'impact':'Denial of Service',
    'severity':'HIGH',
    'curl_verify':''
  }

  q = '''
    query {
        __schema { 
          ...A
        }
    }

    fragment A on __Schema {
        __typename
        ...B
    }

    fragment B on __Schema {
        ...A
    }
'''
  gql_response = graph_query(url, proxies=proxy, headers=headers, payload=q)
  res['curl_verify'] = curlify(gql_response)
  
  try:
    print(gql_response.json())
    if not 'errors' in gql_response.json():
      res['result'] = True
  except:
    pass

  return res