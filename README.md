# GraphQL Cop

## About
GraphQL Cop is a small Python utility to run common security tests against GraphQL APIs.

## Requirements
- Python3
- Requests Library

## Detections
- Alias Overloading (DoS)
- Batch Queries (DoS)
- GET based Queries (CSRF)
- GraphQL Tracing / Debug Modes (Info Leak)
- Field Duplication (DoS)
- Field Suggestions (Info Leak)
- GraphiQL (Info Leak)
- Introspection (Info Leak)
- Directives Overloading (DoS)

## Usage

```
$ python3 graphql-cop.py -t https://mywebsite.com/graphql

                GraphQL Cop 1.0
           Security Auditor for GraphQL
            Dolev Farhi & Nick Aleks
  
Starting...
[HIGH] Introspection Query Enabled (Information Leakage)
[LOW] GraphQL Playground UI (Information Leakage)
[HIGH] Alias Overloading with 100+ aliases is allowed (Denial of Service)
[HIGH] Queries are allowed with 1000+ of the same repeated field (Denial of Service)

python3 main.py -t https://mywebsite.com/graphql -o json

{'Field Suggestions': {'severity': 'LOW', 'impact': 'Information Leakage', 'description': 'Field Suggestions are Enabled'}, 'Introspection': {'severity': 'HIGH', 'impact': 'Information Leakage', 'description': 'Introspection Query Enabled'}, 'Possible CSRF (GET)': {'severity': 'LOW', 'impact': 'Possible CSRF', 'description': 'HTTP GET method supported (maybe CSRF)'}, 'Alias Overloading': {'severity': 'HIGH', 'impact': 'Denial of Service', 'description': 'Alias Overloading with 100+ aliases is allowed'}, 'Field Duplication': {'severity': 'HIGH', 'impact': 'Denial of Service', 'description': 'Queries are allowed with 1000+ of the same repeated field'}, 'Directive Overloading': {'severity': 'HIGH', 'impact': 'Denial of Service', 'description': 'Multiple duplicated directives allowed in a query'}}
```

Using `graphql-cop` through a Proxy (Eg: Burp Suite) and adding custom headers (Eg: Authorization):

```
$ python3 graphql-cop.py -t https://mywebsite.com/graphql --proxy --header '{"Authorizathion": "Bearer token_here"}'

                GraphQL Cop 1.0
           Security Auditor for GraphQL
            Dolev Farhi & Nick Aleks
  
Starting...
[HIGH] Introspection Query Enabled (Information Leakage)
[LOW] GraphQL Playground UI (Information Leakage)
[HIGH] Alias Overloading with 100+ aliases is allowed (Denial of Service)
[HIGH] Queries are allowed with 1000+ of the same repeated field (Denial of Service)
```