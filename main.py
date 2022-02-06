#!/usr/env/python3
import sys

from lib.tests.info_field_suggestions import field_suggestions
from lib.tests.info_introspect import introspection
from lib.tests.info_graphiql import detect_graphiql
from lib.tests.info_get_method_support import get_method_support
from lib.tests.dos_alias_overloading import alias_overloading
from lib.tests.dos_batch import batch_query
from lib.tests.dos_field_duplication import field_duplication
from lib.tests.info_trace_mode import trace_mode
from lib.utils import severity_conversion, is_graphql, draw_art

if len(sys.argv) < 2:
    print(draw_art())
    print('Error: Missing URL.')
    print('e.g. https://mysite.com/graphql')
    sys.exit(1)

url = sys.argv[1]
if not is_graphql(url):
    print(url, 'does not seem to be running GraphQL.')
    sys.exit(1)

print(draw_art())
print('Starting...')
"""
    Field Suggestions
"""
fs_severity = 1
fs_impact = 'Information Leakage'
if field_suggestions(url):
    print('[{}] {} ({})'.format(severity_conversion(fs_severity), 'Field Suggestions is Enabled', fs_impact))

"""
    Introspection
"""
ins_severity = 3
ins_impact = 'Information Leakage'
if introspection(url):
    print('[{}] {} ({})'.format(severity_conversion(ins_severity), 'Introspection Query Enabled', ins_impact))

"""
    Playground
"""
pg_severity = 1
pg_impact = 'Information Leakage'
if detect_graphiql(url):
    print('[{}] {} ({})'.format(severity_conversion(pg_severity), 'GraphQL Playground UI', pg_impact))

"""
    HTTP GET method support (maybe CSRF)
"""
hget_severity = 1
hget_impact = 'Possible CSRF'
if get_method_support(url):
    print('[{}] {} ({})'.format(severity_conversion(hget_severity), 'HTTP GET Method Query Enabled', hget_impact))

"""
    Alias Overloading
"""
alias_severity = 3
alias_impact = 'Denial of Service'
if alias_overloading(url):
    print('[{}] {} ({})'.format(severity_conversion(alias_severity), 'Alias Overloading with 100+ aliases is allowed', alias_impact))

"""
    Batch Queries
"""
batch_severity = 3
batch_impact = 'Denial of Service'
if batch_query(url):
    print('[{}] {} ({})'.format(severity_conversion(batch_severity), 'Batch queries allowed with 10+ simultaneous queries)', batch_impact))


"""
    Field Duplication
"""
dup_severity = 3
dup_impact = 'Denial of Service'
if field_duplication(url):
    print('[{}] {} ({})'.format(severity_conversion(dup_severity), 'Queries are allowed with 1000+ of the same repeated field', dup_impact))

"""
    Tracing mode
"""
trc_severity = 0
trc_impact = 'Information Leakage'
if trace_mode(url):
    print('[{}] {} ({})'.format(severity_conversion(trc_severity), 'Tracing is enabled', trc_impact))

