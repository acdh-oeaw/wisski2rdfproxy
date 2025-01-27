## wisski2rdfproxy

A command-line tool for generating [rdfproxy](https://github.com/acdh-oeaw/rdfproxy) models and queries from [WissKI](https://wiss-ki.eu) paths.

### TODOs / missing implementation

- [ ] add option to name endpoints ([#1](https://github.com/acdh-oeaw/wisski2rdfproxy/issues/1))
- [ ] add support for reverse-traversal of paths (especially across `entity_reference` boundaries)
- [ ] allow `cardinality=1` model fields to be specified as optional
- [ ] assure that binding variable names within queries are actually unique
- [ ] add support for limited-level `.*.*[...]` to `--endpoint_include_fields`
- [ ] implement auto-limiting of recursive embeddings
- [ ] if there is a partial match for an entity in the triple store which is missing some mandatory field, that partial entity will (erroneously) show up in any endpoint which excludes the mandatory field
- [ ] if there is a redundant more specific exclude, the broader exclude is currently disregarded without any warning
- [ ] use a proper parser/serializer (like [larql](https://github.com/lu-pl/larql/)) to generate the SPARQL-queries

### Usage

1. export pathbuilder json or xml (through [web interface](https://wiss-ki.eu/documentation/pathbuilder/export-import-pathbuilder) or [WissKI API](https://github.com/kaiamann/wisski_api))
2. run `./wisski2rdfproxy.py`

```
usage: ./wisski2rdfproxy.py [-h] [-v] [-j wisski_api_export | -x wisski_path_xml]
                            [-ee path_id [exclude_field ...]]
                            [-ei path_id [include_field ...]] [-0]
                            [--cors [CORS ...]] [--custom-query-parameters]
                            [--pagesize PAGESIZE] [-o OUTPUT_PREFIX]
                            [-a sparql_api_url] [-r [AUTO_LIMIT_MODEL_RECURSION]]
                            [-i INDENT] [-ns prefix full_url]

Generate rdfproxy models and queries from WissKI pathbuilder specifications

options:
  -h, --help            show this help message and exit
  -v, --verbose         Increase the verbosity of the logging output: default is
                        WARNING, use -v for INFO, -vv for DEBUG

WissKI pathbuilder input (exactly one is required):
  -j wisski_api_export, --json wisski_api_export
  -x wisski_path_xml, --xml wisski_path_xml

Endpoint/model options:
  specify one or more WissKI path ids for which to generate endpoints (i.e. models + a query).
  If no endpoints are given, lists all available types without generating any endpoints.

  -ee path_id [exclude_field ...], --endpoint-exclude-fields path_id [exclude_field ...]
                        a path id for which to generate an endpoint, followed by 0 or
                        more field paths that should be excluded from the endpoint
                        return value. any fields not in this list will be included by
                        default.
  -ei path_id [include_field ...], --endpoint-include-fields path_id [include_field ...]
                        a path id for which to generate an endpoint, followed by 1 or
                        more field paths that should be included in the endpoint
                        return value.

Output options:
  -0, --everything-optional
                        make all Wisski elements with cardinality=1 optional
  --cors [CORS ...]     allow CORS requests from these origins (default: $(default)s)
  --custom-query-parameters
                        Whether to create a QueryParameters class for every endpoint
  --pagesize PAGESIZE   default page-size of the generated endpoints (default:
                        $(default)s)
  -o OUTPUT_PREFIX, --output-prefix OUTPUT_PREFIX
                        file prefix for the python model and SPARQL query fields that
                        will be generated for each endpoint (default: print both to
                        stdout)
  -a sparql_api_url, --api sparql_api_url
                        also generate FastAPI routes for all endpoints at the
                        output_prefix location, pointing to the given SPARQL endpoint
                        URL
  -r [AUTO_LIMIT_MODEL_RECURSION], --auto-limit-model-recursion [AUTO_LIMIT_MODEL_RECURSION]
                        NOT IMPLEMENTED YET: automatically limit recursive model
                        embeddings to this many levels (off by default)
  -i INDENT, --indent INDENT
                        indentation to use for the SPARQL queries (default: 2 spaces)
  -ns prefix full_url, --namespace prefix full_url
                        namespace replacements to carry out, use a -ns for every
                        prefix specification (default: [['crm', 'http://www.cidoc-
                        crm.org/cidoc-crm/'], ['lrmoo',
                        'http://iflastandards.info/ns/lrm/lrmoo/'], ['star',
                        'https://r11.eu/ns/star/'], ['skos',
                        'http://www.w3.org/2004/02/skos/core#'], ['r11',
                        'https://r11.eu/ns/spec/'], ['r11pros',
                        'https://r11.eu/ns/prosopography/']])

field include/exclude syntax:

  TODO document syntax, how to use for stubs etc
  -ee endpointname some.model.path.somefield some.model.path.otherfield.*

  # exclude all children of that field
  -ee endpointname field.*

  # include all direct children of that field
  -ei endpointname field.*

  # include ALL (direct and indirect) children of that field, i.e. that entire sub-tree
  -ei endpointname field.**

example usage:

  # generate all endpoints
  ./wisski2rdfproxy.py -j wisski-pathbuilder-export.json

  # generate one complete endpoint
  ./wisski2rdfproxy.py -j wisski-pathbuilder-export.json -ee person

  # generate the same endpoint, but don't include some field
  ./wisski2rdfproxy.py -j wisski-pathbuilder-export.json -ee person foo

  # generate two endpoints
  ./wisski2rdfproxy.py -j wisski-pathbuilder-export.json -ee person foo
```
