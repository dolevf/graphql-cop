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

# Usage
```
python3 main.py https://mywebsite.com/graphql

                GraphQL Cop 1.0
           Security Auditor for GraphQL
         Dolev Farhi <dolev@lethalbit.com>
  
Starting...
[HIGH] Introspection Query Enabled (Information Leakage)
[LOW] GraphQL Playground UI (Information Leakage)
[HIGH] Alias Overloading with 100+ aliases is allowed (Denial of Service)
[HIGH] Queries are allowed with 1000+ of the same repeated field (Denial of Service)
```