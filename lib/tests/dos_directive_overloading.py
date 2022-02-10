from lib.utils import graph_query, get_error

def directive_overloading(url):
  result = False
  
  q = 'query { __typename @aa@aa@aa@aa@aa@aa@aa@aa@aa@aa }'
  gql_response = graph_query(url, payload=q)
    
  try:
    if len(gql_response['errors']) == 10:
      result = True
  except:
    pass
  
  return result
