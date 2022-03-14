#!/usr/env/python3
import sys

from optparse import OptionParser
from version import VERSION
from config import HEADERS
from json import loads

from lib.tests.info_field_suggestions import field_suggestions
from lib.tests.info_introspect import introspection
from lib.tests.info_graphiql import detect_graphiql
from lib.tests.info_get_method_support import get_method_support
from lib.tests.dos_alias_overloading import alias_overloading
from lib.tests.dos_batch import batch_query
from lib.tests.dos_field_duplication import field_duplication
from lib.tests.dos_directive_overloading import directive_overloading
from lib.tests.info_trace_mode import trace_mode
from lib.utils import is_graphql, draw_art


parser = OptionParser(usage='%prog -t http://example.com -o json')
parser.add_option('-t', '--target', dest='url', help='target url with the path')
parser.add_option('-H', '--header', dest='header', help='Append Header to the request \'{"Authorizathion": "Bearer eyjt"}\'')
parser.add_option('-o', '--output', dest='output_json', 
                        help='Output results to stdout (JSON)', default=False)
parser.add_option('--proxy', '-x', dest='proxy', action='store_true', default=False, 
                        help='Sends the request throug http://127.0.0.1:8080 proxy')
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
        extra_headers = loads(options.header)
        HEADERS.update(extra_headers)
    except:
        print("Cannot cast %s into header dictionary. Ensure the format \'{\"key\": \"value\"}\'."%(options.header))

url = options.url

if not is_graphql(url, proxy, HEADERS):
    print(url, 'does not seem to be running GraphQL.')
    sys.exit(1)

json_output = {}

if field_suggestions(url, proxy, HEADERS):
# Field Suggestions
    json_output['Field Suggestions'] = {}
    json_output['Field Suggestions']['severity'] = 'LOW'
    json_output['Field Suggestions']['impact'] = 'Information Leakage'
    json_output['Field Suggestions']['description'] = 'Field Suggestions are Enabled'

if introspection(url, proxy, HEADERS):
# Introspection
    json_output['Introspection'] = {}
    json_output['Introspection']['severity'] = 'HIGH'
    json_output['Introspection']['impact'] = 'Information Leakage'
    json_output['Introspection']['description'] = 'Introspection Query Enabled'

if detect_graphiql(url, proxy, HEADERS):
# Playground
    json_output['GraphiQL Playground'] = {}
    json_output['GraphiQL Playground']['severity'] = 'LOW'
    json_output['GraphiQL Playground']['impact'] = 'Information Leakage'
    json_output['GraphiQL Playground']['description'] = 'GraphiQL Explorer Enabled'

if get_method_support(url, proxy, HEADERS):
# HTTP GET method support
    json_output['Possible CSRF (GET)'] = {}
    json_output['Possible CSRF (GET)']['severity'] = 'LOW'
    json_output['Possible CSRF (GET)']['impact'] = 'Possible CSRF'
    json_output['Possible CSRF (GET)']['description'] = 'HTTP GET method supported (maybe CSRF)'
    
if alias_overloading(url, proxy, HEADERS):
# Alias Overloading
    json_output['Alias Overloading'] = {}
    json_output['Alias Overloading']['severity'] = 'HIGH'
    json_output['Alias Overloading']['impact'] = 'Denial of Service'
    json_output['Alias Overloading']['description'] = 'Alias Overloading with 100+ aliases is allowed'

if batch_query(url, proxy, HEADERS):
# Batch Queries
    json_output['Batch Queries'] = {}
    json_output['Batch Queries']['severity'] = 'HIGH'
    json_output['Batch Queries']['impact'] = 'Denial of Service'
    json_output['Batch Queries']['description'] = 'Batch queries allowed with 10+ simultaneous queries)'

if field_duplication(url, proxy, HEADERS):
# Field Duplication
    json_output['Field Duplication'] = {}
    json_output['Field Duplication']['severity'] = 'HIGH'
    json_output['Field Duplication']['impact'] = 'Denial of Service'
    json_output['Field Duplication']['description'] = 'Queries are allowed with 500 of the same repeated field'

if trace_mode(url, proxy, HEADERS):
# Tracing mode
    json_output['Tracing Mode'] = {}
    json_output['Tracing Mode']['severity'] = 'INFORMATIONAL'
    json_output['Tracing Mode']['impact'] = 'Information Leakage'
    json_output['Tracing Mode']['description'] = 'Tracing is enabled'

if directive_overloading(url, proxy, HEADERS):
# Directive Overloading
    json_output['Directive Overloading'] = {}
    json_output['Directive Overloading']['severity'] = 'HIGH'
    json_output['Directive Overloading']['impact'] = 'Denial of Service'
    json_output['Directive Overloading']['description'] = 'Multiple duplicated directives allowed in a query'

if options.output_json == 'json':
    print(json_output)
else:
    for k, v in json_output.items():
        print('[{}] {} - {} ({})'.format(v['severity'], k, v['description'], v['impact']))
