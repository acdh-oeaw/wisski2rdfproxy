from argparse import ArgumentParser
from typing import Callable
from rich import print as rprint
from rich.rule import Rule
from rich.syntax import Syntax

from wisskas.filter import endpoint_exclude_fields, endpoint_include_fields
from wisskas.serialize import serialize_entrypoint, serialize_model, serialize_query
from wisskas.string_utils import parse_endpointspec, path_to_camelcase, path_to_filename
from wisskas.wisski import parse_paths


def register_subcommand(parser: ArgumentParser) -> Callable:
    parser.add_argument(
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

    parser.add_argument(
        "-ee",
        "--endpoint-exclude-fields",
        nargs="+",
        metavar=("path_id[/endpoint/target/path]", "exclude_field"),
        action="append",
        help="a path id for which to generate an endpoint, followed by 0 or more field paths that should be excluded from the endpoint return value. any fields not in this list will be included by default.",
        default=[["external_authority"]],
    )

    parser.add_argument(
        "-ei",
        "--endpoint-include-fields",
        nargs="+",
        metavar=("path_id[/endpoint/target/path]", "include_field"),
        action="append",
        help="a path id for which to generate an endpoint, followed by 1 or more field paths that should be included in the endpoint return value.",
        default=[
            [
                "publication/publication/list",
                "publication_creation.publication_creation_event.*",
                "publication_text_assertion",
            ],
            ["person/person/list", "person_descriptive_name"],
            [
                "person/person/details",
                "person_descriptive_name",
                "person_id_assignment.**",
                # "person_appellation_assertion.*", # this kills it -- because some of the other fields are just none
                "person_appellation_assertion.person_appellation_is.*",
                # "person_appellation_assertion.person_appellation_by", # can trigger read timeout
                # "person_appellation_assertion.person_appellation_by.*", # can trigger read timeout
                "person_kinship_assertion.*",
            ],
            ["written_work", "written_work_label", "work_creation_assertion"],
        ],
    )

    file_output = parser.add_argument_group(
        "File output options",
    )
    file_output.add_argument(
        "-o",
        "--output-prefix",
        help="write generated models and queries to disk, using this output filename prefix",
    )

    file_output.add_argument(
        "-a",
        "--server-address",
        metavar="sparql_api_url",
        default="https://graphdb.r11.eu/repositories/RELEVEN",
        help="also generate FastAPI routes for all endpoints at the --output-prefix location, pointing to the given SPARQL endpoint URL",
    )

    file_output.add_argument(
        "--cors",
        nargs="*",
        default=["*"],
        help="allow CORS requests from these origins (default: %(default)s)",
    )

    file_output.add_argument(
        "--git-endpoint",
        action="store_true",
        default=True,
        help="whether to generate a git health check endpoint a /",
    )

    # include_parser.add_argument("path_id", help="main")
    # include_parser.add_argument(
    #     "fieldspec",
    #     nargs="+",
    #     help="1 or more field paths that should be included in the derived model",
    #     default=[],
    # )

    # exclude_parser.add_argument("path_id", help="main")
    # exclude_parser.add_argument(
    #     "fieldspec",
    #     nargs="*",
    #     help="0 or more field paths that should be excluded in the derived model",
    #     default=[],
    # )
    return main


def main(args):
    _root_types, paths = parse_paths(args.input)
    args.prefix = dict(args.prefix)
    endpoints = {}

    for path_id, *filters in args.endpoint_include_fields:
        if len(filters) == 0:
            raise Exception(
                f"endpoint '{path_id}' is defined using --endpoint-include-fields but is missing any fields to include"
            )
        path_id, endpoint_path = parse_endpointspec(path_id)

        if endpoint_path in endpoints:
            raise RuntimeError(
                f"Endpoint path {endpoint_path} is specified more than once"
            )
        endpoints[endpoint_path] = endpoint_include_fields(
            paths[path_id], filters, path_to_camelcase(endpoint_path)
        )

    for path_id, *filters in args.endpoint_exclude_fields:
        path_id, endpoint_path = parse_endpointspec(path_id)

        if endpoint_path in endpoints:
            raise RuntimeError(
                f"Endpoint path {endpoint_path} is specified more than once"
            )
        endpoints[endpoint_path] = endpoint_exclude_fields(
            paths[path_id],
            filters,
            path_to_camelcase(endpoint_path),
        )

    def print_code(code, language="python"):
        rprint(Syntax(code, language, theme=args.color_theme), "\n")

    def dump_to_file(content, filename):
        print(f"writing {filename}")
        with open(filename, "w") as f:
            f.write(content)

    for path, root in endpoints.items():
        filename = f"{args.output_prefix or ''}_{path_to_filename(path)}"

        # this is the local filename
        root["filename"] = filename.rsplit("/", 1)[-1]
        root["details"] = path.endswith("details")

        model = serialize_model(root)
        query = serialize_query(root, args.prefix)

        if args.output_prefix:
            dump_to_file(model, f"{filename}.py")
            dump_to_file(query, f"{filename}.rq")

        else:
            rprint(Rule(path))
            print_code(model)
            print_code(query, "sparql")

    entrypoint = serialize_entrypoint(
        endpoints, args.server_address, args.git_endpoint, {"origins": args.cors}
    )

    if args.output_prefix and args.server_address:
        dump_to_file(entrypoint, f"{args.output_prefix}.py")
    else:
        rprint(Rule("FastAPI entry point"))
        print_code(entrypoint)
