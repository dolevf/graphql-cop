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

## Installation
Below commands should be executed to install dependencies.
```
python3 -m venv path/to/venv
source path/to/venv/bin/activate
python3 -m pip install -r requirements.txt
```
First command creates a virtual environment in the directory specified by `path/to/venv`.
Second command activates the virtual environment. 
Final command installs all the Python packages listed in the requirements.txt.

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
  -x PROXY, --proxy=PROXY
                        HTTP(S) proxy URL in the form
                        http://user:pass@host:port
  -w, --wordlist        Path to a list of custom GraphQL endpoints.
  -v, --version         Print out the current version and exit.
  -T, --tor             Enable Tor proxy
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

Test a website using `graphql-cop` through a proxy (e.g. Burp Suite listening on 127.0.0.1:8080) with custom headers (e.g. Authorization):

```
$ python3 graphql-cop.py -t https://mywebsite.com/graphql --proxy=http://127.0.0.1:8080 --header '{"Authorization": "Bearer token_here"}'

                GraphQL Cop 1.2
           Security Auditor for GraphQL
            Dolev Farhi & Nick Aleks

Starting...
[HIGH] Introspection Query Enabled (Information Leakage)
[LOW] GraphQL Playground UI (Information Leakage)
[HIGH] Alias Overloading with 100+ aliases is allowed (Denial of Service)
[HIGH] Queries are allowed with 1000+ of the same repeated field (Denial of Service)
```

## Docker Setup and Usage

### Prerequisites
- [Docker](https://www.docker.com/get-started) installed on your machine.

### Building the Docker Image

1. Clone the repository:
```
git clone https://github.com/dolevf/graphql-cop.git
cd graphql-cop
```

2. Build the Docker image:
```
docker build -t graphql-cop:latest .
```

### Running the Docker Container
You can run the Docker container and pass arguments to the graphql-cop script as follows:

```
docker run --rm -it graphql-cop:latest -t <GRAPHQL_ENDPOINT> -H '{"<HEADER_KEY>": "<HEADER_VALUE>"}'
```

### Example
Here’s an example of running the container:
```
docker run --rm -it graphql-cop:latest -t https://example.com/graphql -H '{"Authorization": "Bearer abc123xyz"}'
```
### Note
For a list of all available options, run:
```
docker run --rm -it graphql-cop:latest --help
```

Troubleshooting
1. File Not Found Error: If the container cannot find the script to execute, ensure the repository structure is intact and the Dockerfile is correctly set up.
2. Dependencies Issue: If there are missing dependencies, verify that the requirements.txt file is complete.
