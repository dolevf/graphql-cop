#!/usr/bin/env python3 
import sys

from json import loads, dumps
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
from lib.utils import is_graphql, draw_art, read_custom_wordlist

from termcolor import colored

parser = OptionParser(usage='%prog -t http://example.com -o json')
parser.add_option('-t', '--target', dest='url', help='target url with the path - if a GraphQL path is not provided, GraphQL Cop will iterate through a series of common GraphQL paths')
parser.add_option('-H', '--header', dest='header', action='append', help='Append Header(s) to the request \'{"Authorization": "Bearer eyjt"}\' - Use multiple -H for additional Headers')
parser.add_option('-o', '--output', dest='format',
                        help='json', default=False)
parser.add_option('-f', '--force', dest='forced_scan', action='store_true',
                        help='Forces a scan when GraphQL cannot be detected', default=False)
parser.add_option('-d', '--debug', dest='debug_mode', action='store_true',
                        help='Append a header with the test name for debugging', default=False)
parser.add_option('-x', '--proxy', dest='proxy', default=None,
                  help='HTTP(S) proxy URL in the form http://user:pass@host:port')
parser.add_option('-w', '--wordlist', dest='wordlist', default=False, help='Path to a list of custom GraphQL endpoints')
parser.add_option('--version', '-v', dest='version', action='store_true', default=False,
                        help='Print out the current version and exit.')
parser.add_option('--tor','-T', dest='tor', action='store_true', default=False,
                  help='Sends the request through the Tor network (ensure Tor is running and properly configured)')


options, args = parser.parse_args()

if options.version:
    print('version:', VERSION)
    sys.exit(0)

if not options.url:
    print(draw_art())
    parser.print_help()
    sys.exit(1)

if options.proxy:
    proxy = {
        'http': options.proxy,
        'https': options.proxy
    }
elif options.tor:
    import socks
    import socket

    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 9050)
    socket.socket = socks.socksocket

    proxy = {}
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
    print("URL missing scheme (http:// or https://). Ensure URL contains some scheme.")
    sys.exit(1)
else:
    url = options.url

if options.wordlist:
    endpoints = read_custom_wordlist(options.wordlist)
else:
    endpoints = ['/graphiql', '/playground', '/console', '/graphql']

paths = []
parsed = urlparse(url)

if parsed.path and parsed.path != '/':
    paths.append(url)
else:
     for endpoint in endpoints:
        paths.append(parsed.scheme + '://' + parsed.netloc + endpoint)

tests = [field_suggestions, introspection, detect_graphiql,
         get_method_support, alias_overloading, batch_query,
         field_duplication, trace_mode, directive_overloading,
         circular_query_introspection, get_based_mutation, post_based_csrf,
         unhandled_error_detection]

json_output = []

for path in paths:
    if not is_graphql(path, proxy, HEADERS, options.debug_mode):
        if not options.forced_scan:
            print(path, 'does not seem to be running GraphQL. (Consider using -f to force the scan if GraphQL does exist on the endpoint)')
            continue
        else:
            print('Running a forced scan against the endpoint')
    for test in tests:
        json_output.append(test(path, proxy, HEADERS, options.debug_mode))

json_output = sorted(json_output, key=lambda d: d['title']) 

if options.format == 'json':
    print(dumps(json_output))
else:
    for i in json_output:
        if i['result']:
            print('[{}] {} - {} ({})'.format(colored(i['severity'], i['color'], attrs=['bold']), colored(i['title'], 'white', attrs=['bold']), i['description'], i['impact']))
