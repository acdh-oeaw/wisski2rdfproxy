## wisski2rdfproxy

Generate [rdfproxy](https://github.com/acdh-oeaw/rdfproxy) models and queries from Wisski paths.

### Usage

1. export pathbuilder json or xml (through web interface or [Wisski API](https://github.com/kaiamann/wisski_api))
2. run ./wisski2rdfproxy.py

```
usage: ./wisski2rdfproxy.py [-h] [-v] [-j wisski_api_export | -x wisski_path_xml]
                            [-ns prefix full_url] [-i INDENT]
                            [-ee endpoint_id [exclude_field ...]]
                            [-ei endpoint_id [include_field ...]] [-o OUTPUT_PREFIX]

Generate rdfproxy models and queries from Wisski pathbuilder specifications

options:
  -h, --help            show this help message and exit
  -v, --verbose         Increase the verbosity of the logging output: default is
                        ERROR, use -v for WARNING, -vv for INFO, -vvv for DEBUG
  -j wisski_api_export, --json wisski_api_export
  -x wisski_path_xml, --xml wisski_path_xml
  -ns prefix full_url, --namespace prefix full_url
                        namespace replacements to carry out, use a -ns for every
                        prefix specification (default: [['crm', 'http://www.cidoc-
                        crm.org/cidoc-crm/'], ['lrmoo',
                        'http://iflastandards.info/ns/lrm/lrmoo/'], ['star',
                        'https://r11.eu/ns/star/'], ['skos',
                        'http://www.w3.org/2004/02/skos/core#'], ['r11',
                        'https://r11.eu/ns/spec/'], ['r11pros',
                        'https://r11.eu/ns/prosopography/']])
  -i INDENT, --indent INDENT
                        indentation to use for the python models (default: 4 spaces)
  -ee endpoint_id [exclude_field ...], --endpoint_exclude_fields endpoint_id [exclude_field ...]
                        NOT IMPLEMENTED YET: a path id for which to generate an
                        endpoint, followed by 0 or more of its fields that should be
                        excluded from the endpoint return value. any fields not in
                        this list will be included by default. embedded fields can be
                        specified like this: "person field1 field2.*" etc
  -ei endpoint_id [include_field ...], --endpoint_include_fields endpoint_id [include_field ...]
                        NOT IMPLEMENTED YET: a path id for which to generate an
                        endpoint, followed by 0 or more of its fields that should be
                        included in the endpoint return value model
  -o OUTPUT_PREFIX, --output-prefix OUTPUT_PREFIX
                        file prefix for the python model and SPARQL query fields that
                        will be generated for each endpoint (default: print both to
                        stdout)

field include/exclude syntax:

  TODO document syntax, how to use for stubs etc
  -ee endpointname some.model.path.somefield some.model.path.otherfield.*

example usage:

  # generate all endpoints
  ./wisski2rdfproxy.py -j wisski-pathbuilder-export.json

  # generate one complete endpoint
  ./wisski2rdfproxy.py -j wisski-pathbuilder-export.json -ee person

  # generate the same endpoint, but don't include some field
  ./wisski2rdfproxy.py -j wisski-pathbuilder-export.json -ee person foo

  # generate two endpoints
  ./wisski2rdfproxy.py -j wisski-pathbuilder-export.json -ee person foo

  If no -endpoint_s are specified, generates full endpoints for all model classes by default.
```
