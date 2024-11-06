#!/usr/bin/env python3
# type: ignore

import argparse
from contextlib import nullcontext
import copy
import json
import logging
from os import getenv
from os.path import basename
import sys
import textwrap
import xml.etree.ElementTree as ET

sys.setrecursionlimit(100)


def formatter_class(prog):
    return argparse.RawDescriptionHelpFormatter(
        prog, width=min(int(getenv("COLUMNS", 85)), 85)
    )


parser = argparse.ArgumentParser(
    formatter_class=formatter_class,
    prog="./wisski2rdfproxy.py",
    description="Generate rdfproxy models and queries from WissKI pathbuilder specifications",
    epilog=textwrap.dedent("""\
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
                          %(prog)s -j wisski-pathbuilder-export.json

                          # generate one complete endpoint
                          %(prog)s -j wisski-pathbuilder-export.json -ee person

                          # generate the same endpoint, but don't include some field
                          %(prog)s -j wisski-pathbuilder-export.json -ee person foo

                          # generate two endpoints
                          %(prog)s -j wisski-pathbuilder-export.json -ee person foo"""),
)
parser.add_argument(
    "-v",
    "--verbose",
    action="count",
    default=0,
    help="Increase the verbosity of the logging output: default is WARNING, use -v for INFO, -vv for DEBUG",
)

i = parser.add_argument_group("WissKI pathbuilder input (exactly one is required)")
i = i.add_mutually_exclusive_group()
i.add_argument(
    "-j",
    "--json",
    metavar="wisski_api_export",
    type=argparse.FileType("r"),
    default="examples/releven_assertions_20240821.json",
    help="",
)
i.add_argument(
    "-x", "--xml", metavar="wisski_path_xml", type=argparse.FileType("r"), help=""
)

i = parser.add_argument_group(
    "Endpoint/model options",
    "specify one or more WissKI path ids for which to generate endpoints (i.e. models + a query).\nIf no endpoints are given, lists all available types without generating any endpoints.",
)
i.add_argument(
    "-ee",
    "--endpoint-exclude-fields",
    nargs="+",
    metavar=("path_id", "exclude_field"),
    action="append",
    help="a path id for which to generate an endpoint, followed by 0 or more field paths that should be excluded from the endpoint return value. any fields not in this list will be included by default.",
    default=[],
)
i.add_argument(
    "-ei",
    "--endpoint-include-fields",
    nargs="+",
    metavar=("path_id", "include_field"),
    action="append",
    help="a path id for which to generate an endpoint, followed by 1 or more field paths that should be included in the endpoint return value.",
    default=[],
)

i = parser.add_argument_group("Output options")
i.add_argument(
    "--cors",
    nargs="*",
    default=["*"],
    help="allow CORS requests from these origins (default: $(default)s)",
)
i.add_argument(
    "--pagesize",
    type=int,
    default=10,
    help="default page-size of the generated endpoints (default: $(default)s)",
)
i.add_argument(
    "-o",
    "--output-prefix",
    help="file prefix for the python model and SPARQL query fields that will be generated for each endpoint (default: print both to stdout)",
)
i.add_argument(
    "-a",
    "--api",
    metavar="sparql_api_url",
    default="https://graphdb.r11.eu/repositories/RELEVEN",
    help="also generate FastAPI routes for all endpoints at the output_prefix location, pointing to the given SPARQL endpoint URL",
)
i.add_argument(
    "-r",
    "--auto-limit-model-recursion",
    nargs="?",
    type=int,
    const=1,
    help="NOT IMPLEMENTED YET: automatically limit recursive model embeddings to this many levels (off by default)",
)

i.add_argument(
    "-i",
    "--indent",
    default="    ",
    help="indentation to use for the python models (default: 4 spaces)",
)
i.add_argument(
    "-ns",
    "--namespace",
    nargs=2,
    metavar=("prefix", "full_url"),
    action="append",
    help="namespace replacements to carry out, use a -ns for every prefix specification (default: %(default)s)",
    default=[
        ["crm", "http://www.cidoc-crm.org/cidoc-crm/"],
        ["lrmoo", "http://iflastandards.info/ns/lrm/lrmoo/"],
        ["star", "https://r11.eu/ns/star/"],
        ["skos", "http://www.w3.org/2004/02/skos/core#"],
        ["r11", "https://r11.eu/ns/spec/"],
        ["r11pros", "https://r11.eu/ns/prosopography/"],
    ],
)

args = parser.parse_args()

logging.basicConfig(
    level=max(10, 30 - 10 * args.verbose), format="%(levelname)s: %(message)s"
)
logger = logging.getLogger(__name__)


def parse_filter_list(ls):
    split = [i.split(".", 1) for i in ls]
    prefixes = set(p for p, *_r in split)
    return {p: [r[1] for r in split if r[0] == p and len(r) > 1] for p in prefixes}


wisski_type_map = {
    # TODO add support for all Wisski field types: https://wiss-ki.eu/documentation/pathbuilder/configuration/lists
    "string": "str",
    "list_string": "list[str]",  # FIXME this doesn't get annotated properly, need to change the Type's cardinality instead
    "uri": "AnyUrl",
}


class Field:
    """
    A field has a name (str) and a type (either a str denoting a Python primitive, or an instance of Type)
    """

    def __init__(self, path):
        self.name = path.find("id").text
        # self.prefix = [] # only required when cloning
        self.paths = [process_path(el.text) for el in path.find("path_array")]
        self.group = path.find("group_id").text
        if self.group == "0":
            self.group = None
        self.cardinality = int(path.find("cardinality").text)
        tp = path.find("fieldtype").text

        self.datatype_property = None
        if tp in wisski_type_map:
            self.type = wisski_type_map[
                tp
            ]  # TODO throw error if type is not implemented yet
            self.datatype_property = process_path(path.find("datatype_property").text)
        elif tp == "entity_reference":
            self.type = None  # needs to be resolved
        else:
            self.type = Type(path)

    # return a set of this field's type and all its nested types
    # the result set is built up incrementally to avoid recursion
    def nested_types(self, collection=None):
        if collection is None:
            collection = set()
        if not isinstance(self.type, Type) or self.type in collection:
            return collection
        collection.add(self.type)
        for n in self.type.fields:
            collection = n.nested_types(collection)
        return collection

    def prepare_clone(self, prefix):
        logger.debug(
            f"cloning field {self.name} (type {self.type}) with field prefix {prefix}"
        )
        f = copy.copy(self)
        f.prefix = prefix + [self.name]
        return f

    def clone_exclude(self, exclude, prefix=[]):
        f = self.prepare_clone(prefix)
        if isinstance(self.type, Type):
            if "*" in exclude:
                logger.debug("all fields of this should be excluded")
                f.type = wisski_type_map["uri"]
                f.datatype_property = None
                return f
            try:
                f.type = f.type.clone_exclude(exclude, f.prefix)
            except RecursionError:
                # TODO if args.auto_fix_recursive_embeddings:
                self.handle_recursion(prefix)
        return f

    def clone_include(self, include, prefix=[]):
        f = self.prepare_clone(prefix)
        if isinstance(self.type, Type):
            if include == []:
                logger.debug(
                    f"all fields of {f.name} (and descendants) should be excluded"
                )
                f.type = wisski_type_map["uri"]
                f.datatype_property = None
                return f
            try:
                f.type = f.type.clone_include(include, f.prefix)  # TODO pass '*' down?
            except RecursionError:
                # TODO if args.auto_fix_recursive_embeddings:
                self.handle_recursion(prefix)
        return f

    def handle_recursion(self, prefix):
        # try to find recursion pattern -- identical adjacent sequences of path ids
        for i in range(1, 50):
            try:
                start = next(
                    s
                    for s in range(len(prefix) - i)
                    if prefix[s : s + i] == prefix[s + i : s + 2 * i]
                )
                raise RuntimeError(f"""recursive embedding in endpoint "{prefix[0]}":

  {" -> ".join(prefix[start:start+i+1])}

starting at:

  {"the endpoint's top-level entity" if start == 0 else ".".join(prefix[1:start+1])}

At the very minimum, you probably want to exclude the following path from the endpoint:
   
  {".".join(prefix[1:start+i+1])}.*""")
            except StopIteration:
                pass

        raise RuntimeError(
            f'recursive embedding in endpoint "{prefix[0]}" (unable to locate it, recursion step > 50 ?'
        )

    def anchor(self):
        return f'{"__".join(self.prefix)}'

    def select(self):
        logger.debug(
            f"field select of {self.name} is {self.anchor()} (at {self.prefix})"
        )
        if isinstance(self.type, Type):
            return self.type.select(self.anchor())
        else:
            return [f"?{self.anchor()}"]

    def bindings(self, anchor_var=None):
        logger.debug(
            f"bindings for field {self.name} (anchor {anchor_var}) {self.prefix}"
        )
        var = anchor_var or self.anchor()

        bindings = []
        prevvarname = var
        fullpath = (
            self.paths
            if self.datatype_property is None
            else self.paths + [self.datatype_property]
        )
        # for i in range(int((len(self.paths)) / 2)):
        nsteps = int(len(fullpath) / 2)
        for i in range(nsteps):
            nextvarname = (
                self.anchor()
                if i == nsteps - 1
                else f"{prevvarname}___{self.short_var()}"
            )
            p = fullpath[2 * i + 1]
            bindings.append(
                f"?{nextvarname} {p[1:]} ?{prevvarname}."
                if p.startswith("^")
                else f"?{prevvarname} {p} ?{nextvarname}."
            )
            prevvarname = nextvarname

        if isinstance(self.type, Type):
            bindings = bindings + self.type.bindings(prevvarname)

        # if self.datatype_property != None:
        # bindings.append(f'{prevvarname} {self.datatype_property} {self.anchor()}.')
        if self.datatype_property is None:
            bindings = [f"?{prevvarname} a {self.paths[-1]}."] + bindings

        if (
            self.cardinality == 1 or anchor_var is None
        ):  # ignore cardinality if this is the root field
            return bindings
        else:
            return ["OPTIONAL {", *bindings, "}"]

    def short_var(self):
        return "".join(w[0] for w in self.name.split("_") if len(w))

    def __str__(self):
        # for lists, rdfproxy requires Annotated[list[type], SPARQLBinding(...)], NOT list[Annotated[type, SPARQLBinding(...])]]
        tp = self.type if self.cardinality == 1 else f"list[{self.type}]"
        return f'{self.name}: Annotated[{tp}, SPARQLBinding("{self.anchor()}")]'

    def __gt__(self, other):
        return str(self) > str(other)


class Type:
    """
    A type has an id (really a CamelCase classname, str), a name (str describing the type) and fields (Field[])
    """

    def __init__(self, path):
        self.fields = []
        self.prefix = []
        self.id = path.find("id").text
        self.name = path.find("name").text
        self.paths = [process_path(el.text) for el in path.find("path_array")]

    def classname(self):
        return "_".join(
            map(
                lambda el: el.replace("_", " ").title().replace(" ", ""),
                [self.id] if self.prefix == [] else self.prefix,
            )
        )

    def select(self, anchor_var):
        return [f"?{anchor_var}"] + [
            f"{args.indent}{s}" for f in self.fields for s in f.select()
        ]

    def bindings(self, anchor_var):
        logger.debug(f"bindings for type {self.id} (anchor {anchor_var})")
        bindings = []
        for f in self.fields:
            bindings.extend(
                [""] + [f"{args.indent}{b}" for b in f.bindings(anchor_var)]
            )
        return bindings

    # internal helper fn
    def prepare_clone(self, ls, prefix):
        c = copy.copy(self)
        c.prefix = prefix  # + [self.id]
        logger.debug(f"cloning type {self} with type prefix {c.prefix}")
        split = parse_filter_list(ls)
        for key in split:
            if key == "*" or key == "**":
                if key == "*" and len(c.fields) == 0:
                    logger.warning(
                        f"found '{key}' at {'.'.join(prefix[1:])} even though there are no fields"
                    )
                else:
                    logger.debug(f"clone: found '{key}' in type '{c}'")
                continue
            exists = False
            for f in c.fields:
                if f.name == key:
                    logger.debug(f"clone: found '{key}' in field of '{c.id}'")
                    exists = True
                    break
            if not exists:
                logger.warning(
                    f'unknown field specified in include/exclude list at {".".join(prefix[1:])}: {key}'
                )
        return (c, split)

    # exclude is a list of "*", "fieldname", "fieldname.subfieldname" or "fieldname.*"
    def clone_exclude(self, exclude, prefix=[]):
        c, excludes = self.prepare_clone(exclude, prefix)
        c.fields = [
            f.clone_exclude(excludes.get(f.name, []), c.prefix)
            for f in self.fields
            if excludes.get(f.name, None) != []
        ]
        return c

    def clone_include(self, include, prefix=[]):
        c, includes = self.prepare_clone(include, prefix)
        logger.debug(f"include {self.id}: {[f.name for f in self.fields]}")
        if "**" in include:
            c.fields = [f.clone_include(["**"], c.prefix) for f in self.fields]
        else:
            c.fields = [
                f.clone_include(includes.get(f.name, []), c.prefix)
                for f in self.fields
                if "*" in include or f.name in includes
            ]
        return c

    # return pydantic model definition
    def model(self):
        model = f"""class {self.classname()}(BaseModel):
{args.indent}class Config:
{2*args.indent}title = "{self.name}"
{2*args.indent}model_bool = "{'__'.join(self.prefix)}"
"""
        if any((f.cardinality == -1 for f in self.fields)):
            model += f"{2*args.indent}group_by = \"{'__'.join(self.prefix)}\"\n"

        return model + ("\n".join(f"{args.indent}{f}" for f in self.fields) + "\n")

    # {2*args.indent}original_path_id = "{self.id}"
    # {args.indent}id: Annotated[AnyUrl, SPARQLBinding("{'__'.join(self.prefix)}")]

    # return a set of this type and all its nested types
    # the result set is built up incrementally to avoid recursion
    # def nested_types(self, collection = set()):
    #   if self in collection:
    #     return collection
    #   if len(self.fields):
    #     collection.add(self)
    #   if isinstance(self.type, Type):
    #     # entity_reference
    #     for n in self.type.nested_types():
    #       collection = n.nested_types(collection)
    #   else:
    #     for n in self.fields:
    #       collection = n.nested_types(collection)
    #   return collection

    def __gt__(self, other):
        return str(self) > str(other)

    def __str__(self):
        return self.classname()


if args.json:
    paths = json.load(args.json)
    tree = ET.fromstring(paths["xml"])
    # ET.indent(tree, space="\t", level=0)
    # ET.ElementTree(tree).write("paths.xml", encoding="utf-8")
else:
    tree = ET.parse(args.xml)


def process_path(p):
    for prefix, path in args.namespace:
        p = p.replace(path, f"{prefix}:")
    return p


try:
    paths = {
        p.name: p
        for p in [Field(path) for path in tree if path.find("enabled").text == "1"]
    }
    logger.info(f"Found a total of {len(paths)} enabled paths")

    # create type uri -> Type lookup dict
    root_types = {m.type.paths[-1]: m.type for m in paths.values() if m.group is None}
    expected_n_root_classes = len([t for t in paths.values() if t.group is None])
    if len(root_types) != expected_n_root_classes:
        raise RuntimeError(
            f"there are {expected_n_root_classes} root paths, but only {len(root_types)}"
        )

    for p in paths.values():
        if p.type is None:
            # Upgrade to your own type
            entity_type = p.paths[-1]
            try:
                p.type = root_types[entity_type]
                logger.debug(
                    f'resolved entity_reference field {p.name} from rdf class "{entity_type}" to model type "{p.type}"'
                )
            except KeyError:
                logger.warning(
                    f"field {p.name} is an entity reference, but couldn't find a model for the last element of its path ({entity_type})"
                )
                p.type = None
                # del types[f.id] ?

        # collect all field dependencies
        if p.group is not None:
            try:
                paths[p.group].type.fields.append(p)
            except KeyError:
                logger.warning(f"{p.id} is part of group {p.group} which doesn't exist")
                # TODO remove type?

    if len(args.endpoint_include_fields) + len(args.endpoint_exclude_fields) == 0:
        print(
            f"\nno endpoints specified. here are all {len(paths)} path ids that endpoints could be generated for:\n"
        )
        for p in sorted(paths):
            print(f" - {p}")
        print(
            f"\nthese are the {len(root_types)} path ids that are top-level types (and their corresponding rdf classes):\n"
        )
        for p in sorted([(t.id, rdftype) for rdftype, t in root_types.items()]):
            print(f" - {p[0]} ({p[1]})")
        sys.exit(0)

    def write_endpoint(name, t):
        required_types = sorted(t.nested_types())
        logger.debug(
            f"endpoint {name} requires the following types: {[t.id for t in required_types]}"
        )
        with open(
            f"{args.output_prefix}_{name}.py", "w"
        ) if args.output_prefix else nullcontext(sys.stdout) as py:
            with open(
                f"{args.output_prefix}_{name}.rq", "w"
            ) if args.output_prefix else nullcontext(sys.stdout) as rq:
                if py != sys.stdout:
                    py.write(
                        "from pydantic import BaseModel, AnyUrl\nfrom rdfproxy import SPARQLBinding\nfrom typing import Annotated\n\n"
                    )

                for n in reversed(required_types):
                    py.write(n.model())
                    py.write("\n\n")

                for prefix, url in args.namespace:
                    rq.write(f"PREFIX {prefix}: <{url}>\n")
                # work around GraphDB API not allowing line breaks in the SELECT (throwing weird 'variable not present in GROUP BY' error)
                rq.write("\nSELECT\n")
                for s in t.select():
                    rq.write(f"{s}\n")
                rq.write("\nWHERE {\n")
                rq.write("\n".join(t.bindings()))
                rq.write("\n}\n\n")

        logger.info(
            f'Generated endpoint "{name}", consisting of {len(required_types)} nested model class(es)'
        )

    for n, *fields in args.endpoint_include_fields:
        if len(fields) == 0:
            raise Exception(
                f"endpoint '{n}' is defined using --endpoint-include-fields but is missing any fields to include"
            )
    endpoints = {
        n: paths[n].clone_exclude(fields) for n, *fields in args.endpoint_exclude_fields
    } | {
        n: paths[n].clone_include(fields) for n, *fields in args.endpoint_include_fields
    }

    # write to files or stdout
    for name, endpoint_types in endpoints.items():
        write_endpoint(name, endpoint_types)

    if args.output_prefix and args.api:
        with open(f"{args.output_prefix}.py", "w") as py:
            py.write(
                textwrap.dedent("""                from fastapi import FastAPI
                from os import path
                from rdfproxy import Page, SPARQLModelAdapter

                app = FastAPI()
                """)
            )
            if len(args.cors):
                py.write(
                    textwrap.dedent(f"""
                from fastapi.middleware.cors import CORSMiddleware

                app.add_middleware(
                    CORSMiddleware,
                    allow_origins={str(args.cors)},
                    allow_credentials=True,
                    allow_methods=["*"],
                    allow_headers=["*"],
                )
                """)
                )
            for name, root_type in endpoints.items():
                py.write(f"""\n\nfrom {basename(args.output_prefix)}_{name} import {root_type.type.classname()}
@app.get("/{name}/")
def {name}(page : int = 1, size : int = {args.pagesize}) -> Page[{root_type.type.classname()}]:
{args.indent}adapter = SPARQLModelAdapter(
{2*args.indent}target="{args.api}",
{2*args.indent}query=open(f"{{path.dirname(path.realpath(__file__))}}/{basename(args.output_prefix)}_{name}.rq").read().replace('\\n ', ' '),
{2*args.indent}model={root_type.type.classname()})
{args.indent}return adapter.query(page=page, size=size)
""")
            print(f"FastAPI routes written to {args.output_prefix}.py")
            print("run the following:")
            print(f"$ fastapi dev {args.output_prefix}.py")

    if not args.output_prefix:
        print(
            "\nOutput is informational only, use the -o argument to write the models and queries to file(s)"
        )

except RuntimeError as e:
    logger.error(e)
    sys.exit(1)
