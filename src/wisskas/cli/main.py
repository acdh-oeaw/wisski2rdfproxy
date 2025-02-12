import argparse
import logging
from typing import Callable

from rich_argparse import RichHelpFormatter

from wisskas.cli.endpoints import register_subcommand as endpoints_args
from wisskas.cli.paths import register_subcommand as paths_args


def main():
    parser = argparse.ArgumentParser(formatter_class=RichHelpFormatter)
    parser.add_argument(
        "-input",
        type=argparse.FileType("r"),
        default="tests/data/releven_assertions_20240821.xml",
        help="a WissKI pathbuilder file",
    )

    subparsers = parser.add_subparsers(
        title="CLI commands",
        required=True,
    )

    def add_command(command: str, add_subcommand_args: Callable, **kwargs):
        subparser = subparsers.add_parser(
            command,
            help="show information about WissKI paths",
            formatter_class=RichHelpFormatter,
            **kwargs,
        )
        command_main = add_subcommand_args(subparser)
        # TODO check if a callable was returned
        subparser.set_defaults(func=command_main)

        return subparser

    add_command("endpoints", endpoints_args)
    add_command("paths", paths_args)
    # endpoints.add_arguments(
    # subparsers.add_parser(
    #     "endpoints",
    #     help="generate models, queries and FastAPI endpoints",
    #     #     "specify one or more WissKI path ids for which to generate endpoints (i.e. models + a query).\nIf no endpoints are given, lists all available types without generating any endpoints.",
    #     formatter_class=RichHelpFormatter,
    # )
    # )
    # # include_parser = subparsers.add_parser(
    # #     "filter_include",
    # #     help="derive a limited nested model based on including fields",
    # #     formatter_class=RichHelpFormatter,
    # # )
    # # exclude_parser = subparsers.add_parser(
    # #     "filter_exclude",
    # #     help="derive a limited nested model based on excluding fields",
    #     formatter_class=RichHelpFormatter,
    # )

    cli_output = parser.add_argument_group(
        "CLI options",
    )
    cli_output.add_argument(
        "--color-theme",
        default="dracula",
        help="color scheme to use for console output syntax highlighting (see https://pygments.org/docs/styles/#getting-a-list-of-available-styles)",
    )

    cli_output.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase the verbosity of the logging output: default is WARNING, use -v for INFO, -vv for DEBUG",
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=max(10, 30 - 10 * args.verbose), format="%(levelname)s: %(message)s"
    )

    # call subcommand
    args.func(args)
