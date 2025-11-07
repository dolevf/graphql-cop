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

tests = {
    "field_suggestions":field_suggestions,
    "introspection":introspection,
    "detect_graphiql":detect_graphiql,
    "get_method_support":get_method_support, 
    "alias_overloading":alias_overloading,
    "batch_query":batch_query,
    "field_duplication":field_duplication,
    "trace_mode":trace_mode,
    "directive_overloading":directive_overloading,
    "circular_query_introspection":circular_query_introspection,
    "get_based_mutation":get_based_mutation,
    "post_based_csrf":post_based_csrf,
    "unhandled_error_detection":unhandled_error_detection
}