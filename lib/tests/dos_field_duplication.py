from lib.utils import graph_query

def field_duplication(url):
  result = False

  duplicated_string = '__typename \n' * 10000
  q = 'query { ' + duplicated_string + '} '
  gql_response = graph_query(url, payload=q)
  try:
    if gql_response['data']['__typename']:
      result = True
  except:
    pass
  
  return result