# GraphQL Cop - Security Audit Utility for GraphQL

<p align="center">
  <img src="https://github.com/dolevf/graphql-cop/blob/main/static/images/logo.png?raw=true" width="500px" alt="GraphQL Cop"/>
</p>


## About
GraphQL Cop is a small Python utility to run common security tests against GraphQL APIs. GraphQL Cop is perfect for running CI/CD checks in GraphQL. It is lightweight, and covers interesting security issues in GraphQL.

GraphQL Cop allows you to reproduce the findings by providing cURL commands upon any identified vulnerabilities. 

## Requirements
- Python3
- Requests Library

## Detections
- Alias Overloading (DoS)
- Batch Queries (DoS)
- GET based Queries (CSRF)
- POST based Queries using urlencoded payloads (CSRF)
- GraphQL Tracing / Debug Modes (Info Leak)
- Field Duplication (DoS)
- Field Suggestions (Info Leak)
- GraphiQL (Info Leak)
- Introspection (Info Leak)
- Directives Overloading (DoS)
- Circular Query using Introspection (DoS)
- Mutation support over GET methods (CSRF)

## Usage

```
$ python graphql-cop.py -h

Usage: graphql-cop.py -t http://example.com -o json

Options:
  -h, --help            show this help message and exit
  -t URL, --target=URL  target url with the path - if a GraphQL path is not
                        provided, GraphQL Cop will iterate through a series of
                        common GraphQL paths
  -H HEADER, --header=HEADER
                        Append Header(s) to the request '{"Authorization":
                        "Bearer eyjt"}' - Use multiple -H for additional
                        Headers
  -o FORMAT, --output=FORMAT
                        json
  -f, --force           Forces a scan when GraphQL cannot be detected
  -d, --debug           Append a header with the test name for debugging
  -x, --proxy           Sends the request through http://127.0.0.1:8080 proxy
  -v, --version         Print out the current version and exit.
```

Test a website

```
$ python3 graphql-cop.py -t https://mywebsite.com/graphql

                GraphQL Cop 1.1
           Security Auditor for GraphQL
            Dolev Farhi & Nick Aleks

Starting...
[HIGH] Introspection Query Enabled (Information Leakage)
[LOW] GraphQL Playground UI (Information Leakage)
[HIGH] Alias Overloading with 100+ aliases is allowed (Denial of Service)
[HIGH] Queries are allowed with 1000+ of the same repeated field (Denial of Service)
```

Test a website, dump to a parse-able JSON output, cURL reproduction command
```
python3 graphql-cop.py -t https://mywebsite.com/graphql -o json

 {'curl_verify': 'curl -X POST -H "User-Agent: graphql-cop/1.2" -H '
                 '"Accept-Encoding: gzip, deflate" -H "Accept: */*" -H '
                 '"Connection: keep-alive" -H "Content-Length: 33" -H '
                 '"Content-Type: application/json" -d \'{"query": "query { '
                 '__typename }"}\' \'http://localhost:5013/graphql\'',
  'description': 'Tracing is Enabled',
  'impact': 'Information Leakage',
  'result': False,
  'severity': 'INFO',
  'color': 'green',
  'title': 'Trace Mode'},
 {'curl_verify': 'curl -X POST -H "User-Agent: graphql-cop/1.2" -H '
                 '"Accept-Encoding: gzip, deflate" -H "Accept: */*" -H '
                 '"Connection: keep-alive" -H "Content-Length: 64" -H '
                 '"Content-Type: application/json" -d \'{"query": "query { '
                 '__typename @aa@aa@aa@aa@aa@aa@aa@aa@aa@aa }"}\' '
                 "'http://localhost:5013/graphql'",
  'description': 'Multiple duplicated directives allowed in a query',
  'impact': 'Denial of Service',
  'result': True,
  'severity': 'HIGH',
  'color': 'red',
  'title': 'Directive Overloading'}]
```

Test a website using `graphql-cop` through a proxy (e.g. Burp Suite) with custom headers (e.g. Authorization):

```
$ python3 graphql-cop.py -t https://mywebsite.com/graphql --proxy --header '{"Authorization": "Bearer token_here"}'

                GraphQL Cop 1.2
           Security Auditor for GraphQL
            Dolev Farhi & Nick Aleks

Starting...
[HIGH] Introspection Query Enabled (Information Leakage)
[LOW] GraphQL Playground UI (Information Leakage)
[HIGH] Alias Overloading with 100+ aliases is allowed (Denial of Service)
[HIGH] Queries are allowed with 1000+ of the same repeated field (Denial of Service)
```
