#!/usr/env/python3
import sys

from json import loads
from optparse import OptionParser
from version import VERSION
from config import HEADERS
from urllib.parse import urlparse

from lib.tests.info_field_suggestions import field_suggestions
from lib.tests.info_introspect import introspection
from lib.tests.info_graphiql import detect_graphiql
from lib.tests.info_get_method_support import get_method_support
from lib.tests.dos_alias_overloading import alias_overloading
from lib.tests.dos_batch import batch_query
from lib.tests.dos_field_duplication import field_duplication
from lib.tests.dos_directive_overloading import directive_overloading
from lib.tests.info_trace_mode import trace_mode
from lib.tests.dos_circular_introspection import circular_query_introspection
from lib.tests.info_get_based_mutation import get_based_mutation
from lib.tests.info_post_based_csrf import post_based_csrf
from lib.tests.info_unhandled_error import unhandled_error_detection
from lib.utils import is_graphql, draw_art


parser = OptionParser(usage='%prog -t http://example.com -o json')
parser.add_option('-t', '--target', dest='url', help='target url with the path')
parser.add_option('-H', '--header', dest='header', action='append', help='Append Header(s) to the request \'{"Authorization": "Bearer eyjt"}\' - Use multiple -H for multiple Headers')
parser.add_option('-o', '--output', dest='format',
                        help='json', default=False)
parser.add_option('--proxy', '-x', dest='proxy', action='store_true', default=False,
                        help='Sends the request through http://127.0.0.1:8080 proxy')
parser.add_option('--version', '-v', dest='version', action='store_true', default=False,
                        help='Print out the current version and exit.')

options, args = parser.parse_args()

if options.version:
    print('version:', VERSION)
    sys.exit(0)

if not options.url:
    print(draw_art())
    parser.print_help()
    sys.exit(1)

if options.proxy == True:
    proxy = {
        'http':  'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080',
    }
else:
    proxy = {}

if options.header != None:
    try:
        for l in options.header:
            extra_headers = loads(l)
            HEADERS.update(extra_headers)
    except:
        print("Cannot cast %s into header dictionary. Ensure the format \'{\"key\": \"value\"}\'."%(options.header))

if not urlparse(options.url).scheme:
    print("URL missing scheme (http:// or https://). Ensure ULR contains some scheme.")
    sys.exit(1)
else:
    url = options.url

if not is_graphql(url, proxy, HEADERS):
    print(url, 'does not seem to be running GraphQL.')
    sys.exit(1)

tests = [field_suggestions, introspection, detect_graphiql,
         get_method_support, alias_overloading, batch_query,
         field_duplication, trace_mode, directive_overloading,
         circular_query_introspection, get_based_mutation, post_based_csrf,
         unhandled_error_detection]

json_output = []

for test in tests:
    json_output.append(test(url, proxy, HEADERS))

if hasattr(detect_graphiql, 'GraphQLIDEpath'):
    url = detect_graphiql.GraphQLIDEpath
    json_output.append(trace_mode(url, proxy, HEADERS))
    json_output.append(unhandled_error_detection(url, proxy, HEADERS))

if options.format == 'json':
    for i in range(len(json_output)):
        print(json_output[i], end='\n\n')
else:
    for i in json_output:
        if i['result']:
            print('[{}] {} - {} ({})'.format(i['severity'], i['title'], i['description'], i['impact']))
