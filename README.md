# GraphQL Cop

# About
GraphQL Cop is a small Python utility to run common security tests against GraphQL APIs.

# Requirements
- Python3
- Requests Library

# Detections
- Alias Overloading (DoS)
- Batch Queries (DoS)
- GET based Queries (CSRF)
- GraphQL Tracing / Debug Modes (Info Leak)
- Field Duplication (DoS)
- Field Suggestions (Info Leak)
- GraphiQL (Info Leak)
- Introspection (Info Leak)

