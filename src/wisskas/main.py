import argparse
import logging

from wisskas.serialize import serialize_model, serialize_query
from wisskas.wisski import parse_paths

parser = argparse.ArgumentParser()
parser.add_argument(
    "--input",
    type=argparse.FileType("r"),
    default="releven_assertions_20240821.xml",
    help="a WissKI pathbuilder file",
)
parser.add_argument("--output", type=str, help="output filename")

endpoint_parser = parser.add_argument_group(
    "Endpoint/model options",
    "specify one or more WissKI path ids for which to generate endpoints (i.e. models + a query).\nIf no endpoints are given, lists all available types without generating any endpoints.",
)

endpoint_parser.add_argument(
    "-p",
    "--prefix",
    nargs=2,
    metavar=("prefix", "full_url"),
    action="append",
    help="namespace replacements to carry out, use a --prefix for every prefix specification (default: %(default)s)",
    default=[
        ["crm", "http://www.cidoc-crm.org/cidoc-crm/"],
        ["lrmoo", "http://iflastandards.info/ns/lrm/lrmoo/"],
        ["star", "https://r11.eu/ns/star/"],
        ["skos", "http://www.w3.org/2004/02/skos/core#"],
        ["r11", "https://r11.eu/ns/spec/"],
        ["r11pros", "https://r11.eu/ns/prosopography/"],
    ],
)
endpoint_parser.add_argument(
    "-ei",
    "--endpoint-include-fields",
    nargs="+",
    metavar=("path_id[/endpoint/target/path]", "include_field"),
    action="append",
    help="a path id for which to generate an endpoint, followed by 1 or more field paths that should be included in the endpoint return value.",
    default=[["publication"]],
)

parser.add_argument(
    "-v",
    "--verbose",
    action="count",
    default=0,
    help="Increase the verbosity of the logging output: default is WARNING, use -v for INFO, -vv for DEBUG",
)

args = parser.parse_args()
args.prefix = dict(args.prefix)

logging.basicConfig(
    level=max(10, 30 - 10 * args.verbose), format="%(levelname)s: %(message)s"
)

root_types, paths = parse_paths(args.input)

for path_id, *filters in args.endpoint_include_fields:
    # TODO filter

    model = serialize_model(paths[path_id])
    query = serialize_query(paths[path_id], args.prefix)

    if args.output:
        # TODO write to file(s)
        pass

    else:
        print(model)
        print(query)

if args.output:
    # TODO write fastapi entry point
    pass
