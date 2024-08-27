#!/usr/bin/env python3
# type: ignore

import argparse
from contextlib import nullcontext
import copy
import json
import logging
from os import getenv
import sys
import textwrap
import xml.etree.ElementTree as ET

formatter_class=lambda prog: argparse.RawDescriptionHelpFormatter(prog, width=min(int(getenv('COLUMNS', 85)), 85))
parser = argparse.ArgumentParser(formatter_class=formatter_class,
                    prog='./wisski2rdfproxy.py',
                    description='Generate rdfproxy models and queries from Wisski pathbuilder specifications',
                    epilog=textwrap.dedent('''\
                        field include/exclude syntax:

                          TODO document syntax, how to use for stubs etc
                          -ee endpointname some.model.path.somefield some.model.path.otherfield.*

                        example usage:

                          # generate all endpoints
                          %(prog)s -j wisski-pathbuilder-export.json

                          # generate one complete endpoint
                          %(prog)s -j wisski-pathbuilder-export.json -ee person

                          # generate the same endpoint, but don't include some field
                          %(prog)s -j wisski-pathbuilder-export.json -ee person foo

                          # generate two endpoints
                          %(prog)s -j wisski-pathbuilder-export.json -ee person foo

                          If no -endpoint_s are specified, generates full endpoints for all model classes by default.'''))
parser.add_argument('-v', '--verbose', action='count', default=2, help='Increase the verbosity of the logging output: default is ERROR, use -v for WARNING, -vv for INFO, -vvv for DEBUG')
i = parser.add_mutually_exclusive_group()#required=True)
i.add_argument('-j', '--json', metavar='wisski_api_export', type=argparse.FileType('r'), default='examples/releven_assertions_20240821.json', help='')
i.add_argument('-x', '--xml', metavar='wisski_path_xml', type=argparse.FileType('r'), help='')
parser.add_argument('-ns', '--namespace', nargs=2, metavar=('prefix', 'full_url'), action='append', help="namespace replacements to carry out, use a -ns for every prefix specification (default: %(default)s)", default=[['crm', 'http://www.cidoc-crm.org/cidoc-crm/'], ['lrmoo', 'http://iflastandards.info/ns/lrm/lrmoo/'], ['star', 'https://r11.eu/ns/star/'], ['skos', 'http://www.w3.org/2004/02/skos/core#'], ['r11', 'https://r11.eu/ns/spec/'], ['r11pros', 'https://r11.eu/ns/prosopography/']])
parser.add_argument('-ee', '--endpoint_exclude_fields', nargs='+', metavar=('endpoint_id', 'exclude_field'), action='append', help='a path id for which to generate an endpoint, followed by 0 or more field paths that should be excluded from the endpoint return value. any fields not in this list will be included by default.', default=[])
parser.add_argument('-ei', '--endpoint_include_fields', nargs='+', metavar=('endpoint_id', 'include_field'), action='append', help='a path id for which to generate an endpoint, followed by 1 or more field paths that should be included in the endpoint return value.', default=[])
# TODO implement
# parser.add_argument('-a', '--auto-fix-recursive-embeddings', action='store_true', help='automatically fix embeddings')
parser.add_argument('-o', '--output-prefix', help='file prefix for the python model and SPARQL query fields that will be generated for each endpoint (default: print both to stdout)')
parser.add_argument('-i', '--indent', default='    ', help='indentation to use for the python models (default: 4 spaces)')

args = parser.parse_args()

logging.basicConfig(level=max(10, 40 - 10*args.verbose), format = '%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def parse_filter_list(ls):
  split = [ i.split('.', 1) for i in ls ]
  prefixes = set(p for p, *_r in split)
  return { p: [ r[1] for r in split if r[0] == p and len(r) > 1 ] for p in prefixes }

wisski_type_map = {
    # TODO add support for all Wisski field types: https://wiss-ki.eu/documentation/pathbuilder/configuration/lists
    'string': 'str',
    'list_string': 'list[str]', # FIXME this doesn't get annotated properly
    'uri': 'AnyUrl'
    }

class Type:
  def __init__(self, path):
    self.fields = []
    self.id = path.find('id').text
    # id might change during cloning, field name should stay the same
    self.field_name = self.clean_id().replace(' ', '_')
    self.cardinality = int(path.find('cardinality').text)
    self.name = path.find('name').text

    self.paths  = [process_path(el.text) for el in path.find('path_array')]
    self.group = path.find('group_id').text
    if self.group == '0':
      self.group = None

    self.type = path.find('fieldtype').text
    if self.type in wisski_type_map:
      self.type = wisski_type_map[self.type]
    self.datatype_property = process_path(path.find('datatype_property').text)
    # if self.datatype != 'empty':
      # self.type = process_path(self.datatype)

  def clean_id(self):
    return self.id.translate({ord(i): ' ' for i in '*()/_'})

  def camel_id(self):
    return self.clean_id().title().replace(' ', '')

  def short_var(self):
    return ''.join(w[0] for w in self.clean_id().split(' ') if len(w))

  # def clean_name(self):
    # self.cleanname = self.name.lower().translate({ord(i): None for i in '*()/_'}).strip()
  def binding_name(self):
    return self.clean_id().replace(' ', '')

  def is_class(self):
    return self.datatype_property == 'empty'
    # return self.type == entity_reference

  def anchor(self):
    return f'?{self.id}'

  def query(self):
    return f'SELECT {", ".join(self.select())} {{ {"".join(self.bindings())} }}'

  def select(self):
    return [ f.anchor() for f in self.fields ]

  def bindings(self):
    bindings = [f'{self.anchor()} a {self.paths[-1]}.']
    for f in self.fields:
      if f.is_class():
        prevvarname = self.anchor()
        fieldbindings = []
        for i in range(int((len(f.paths)) / 2)):
          nextvarname = f.anchor() if 2*(i+1)+1 == len(f.paths) else f'?{self.short_var()}_{"_" * i}{f.short_var()}'
          p = f.paths[2*i + 1]
          fieldbindings.append(f'{nextvarname} {p[1:]} {prevvarname}.' if p.startswith('^') else f'{prevvarname} {p} {nextvarname}.')
          prevvarname = nextvarname
      else:
        fieldbindings = [f'{self.anchor()} {f.datatype_property} {f.anchor()}.' ]
        # FIXME need to include path, not just datatype_property?
        # try:
          # fieldbindings.append(f'{prevvarname} {f.property} {f.anchor()}.')
        # except AttributeError:
          # logger.warning(f'failed to bind {f.id} in {self.id}')
          # pass

      if f.cardinality == 1:
        bindings.append('\n'.join(fieldbindings))
      else:
        bindings.append(f'OPTIONAL ( {"".join(fieldbindings)} )')
    return bindings

  # internal helper fn
  def prepare_clone(self, ls, prefix):
    c = copy.copy(self)
    c.prefix = prefix + [c.field_name]
    c.id = '_'.join(c.prefix)
    split = parse_filter_list(ls)
    # TODO warn if any path of the split filter list does not exist at this level
    for key in split:
      if key == '*':
        continue
      exists = False
      for f in self.fields:
        if f.id == key or isinstance(f.type, Type) and f.type.id == key:
          exists = True
          break
      if not exists:
        logger.warning(f'unknown field specified in include/exclude list: {".".join(prefix[1:] + [key])}')
    return (c, split)

  def handle_recursion(self, prefix):
    # try to find recursion pattern -- identical adjacent sequences of path ids
    for i in range(1, 50):
      try:
        start = next(s for s in range(len(prefix) - i) if prefix[s:s+i] == prefix[s+i:s+2*i])
        raise RuntimeError(f'recursive embedding in endpoint "{prefix[0]}":\n\n  {" -> ".join(prefix[start:start+i+1])}\n\nstarting at:\n\n  {".".join(prefix[1:start+1])}\n\nAt the very minimum, you probably want to exclude the following path:\n\n  {".".join(prefix[1:start+i+1])}.*')
      except StopIteration:
        pass

    raise RuntimeError(f"recursive embedding in endpoint \"{prefix[0]}\" (unable to locate it, recursion step > 50 ?")


  # exclude is a list of "*", "fieldname", "fieldname.subfieldname" or "fieldname.*"
  def clone_exclude(self, exclude, prefix=[]):
    c, excludes = self.prepare_clone(exclude, prefix)

    if '*' in exclude:
      c.fields = []
      c.type = wisski_type_map['uri']
      return c

    # while True: # for retrying on exception
    try:
      # resolve entity_references -- recursion might happen here!
      if isinstance(c.type, Type):
        return c.type.clone_exclude(exclude, c.prefix)

      c.fields = [ f.clone_exclude(excludes.get(f.field_name, []), c.prefix) for f in self.fields if excludes.get(f.field_name, None) != [] ]
      return c

    except RecursionError:
      # TODO if args.auto_fix_recursive_embeddings:
      self.handle_recursion(prefix)

  def clone_include(self, include, prefix=[]):
    c, includes = self.prepare_clone(include, prefix)

    # resolve entity_references -- recursion might happen here!
    try:
      if isinstance(c.type, Type):
        c.type = c.clone_include(include, prefix)

        c.fields = [ f.clone_include(includes.get(f.field_name, []), c.prefix) for f in self.fields if '*' in include or includes.get(f.field_name, None) != [] ]
        return c
    except RecursionError:
      # TODO if args.auto_fix_recursive_embeddings:
      self.handle_recursion(prefix)

  # return pydantic model definition
  def model(self):
    return f'''class {self.camel_id()}(BaseModel):
{args.indent}class Config:
{2*args.indent}title = "{self.name}"
''' + ('\n'.join(f'{args.indent}{f.field()}' for f in self.fields) + '\n')
# {2*args.indent}rdfproxy_anchor = "?{self.id}"

  # return a set of this type and all its nested types
  # the result set is built up incrementally to avoid recursion
  def nested_types(self, collection = set()):
    if self in collection:
      return collection
    if len(self.fields):
      collection.add(self)
    if isinstance(self.type, Type):
      # entity_reference
      for n in self.type.nested_types():
        collection = n.nested_types(collection)
    else:
      for n in self.fields:
        collection = n.nested_types(collection)
    return collection

  def __gt__(self, other):
    return self.id > other.id

  def __str__(self):
    return str(self.type)
    # return str(self.type) + '\n'.join([ str(f) for f in self.fields ])

  def field(self):
    if self.cardinality == 1:
      return f'{self.field_name}: Annotated[{self.type}, SPARQLBinding("{self.anchor()}")]'
    else:
      return f'{self.field_name}: list[Annotated[{self.type}, SPARQLBinding("{self.anchor()}")]]'


if args.json:
  paths = json.load(args.json)
  tree = ET.fromstring(paths['xml'])
  # ET.indent(tree, space="\t", level=0)
  # ET.ElementTree(tree).write("paths.xml", encoding="utf-8")
else:
  tree = ET.parse(args.xml)

def process_path(p):
  for prefix, path in args.namespace:
    p = p.replace(path, f"{prefix}:") 
  return p

types = { t.id: t for t in [ Type(path) for path in tree if path.find('enabled').text == '1' ] }
logger.info(f'Found a total of {len(types)} enabled types')

# create type uri -> Type lookup dict
root_classes = { m.paths[-1]: m for m in types.values() if m.group == None }

for t in types.values():
  # if t.type == None:
    # Upgrade to your own type
    # t.type = t.camel_id()
  if t.type == 'entity_reference':
    # look up entity_references
    entity_type = t.paths[-1]
    try:
      t.type = root_classes[entity_type]
      logger.debug(f'resolved field {t.id} from {entity_type} -> {t.type}')
    except KeyError:
      logger.warning(f"field {t.id} is an entity reference, but couldn't find a model for the last element of its path ({entity_type})")
      t.type = None
      # del types[f.id] ?

  # collect all field dependencies
  if t.group != None:
    try:
      types[t.group].fields.append(t)
    except KeyError:
      logger.warning(f"{t.id} is part of group {t.group} which doesn't exist")
      # TODO remove type?

if len(args.endpoint_include_fields) + len(args.endpoint_exclude_fields) == 0:
  args.endpoint_exclude_fields = [ [ t.id ] for t in types.values() if t.is_class() ]
  logger.info(f'no endpoints specified, generating full endpoints for all {len(args.endpoint_exclude_fields)} models')
  args.endpoint_exclude_fields = [['person']]

def write_endpoint(name, t):
  required_types = sorted(t.nested_types())
  with open(f'{args.output_prefix}_{name}.py', 'w') if args.output_prefix else nullcontext(sys.stdout) as py:
    with open(f'{args.output_prefix}_{name}.rq', 'w') if args.output_prefix else nullcontext(sys.stdout) as rq:

      if py != sys.stdout:
        py.write('from pydantic import BaseModel, AnyUrl\nfrom rdfproxy import SPARQLBinding\n\n')

      selects = []
      bindings = []
      for n in required_types:
        py.write(n.model())
        py.write('\n\n')
        selects = selects + n.select()
        bindings = bindings + n.bindings()
      for prefix, url in args.namespace:
        rq.write(f'PREFIX {prefix}: <{url}>\n')
      rq.write(f'\nSELECT {" ".join(selects)}\n{{\n')
      rq.write("\n".join(bindings))
      rq.write('\n}\n\n')

  logger.info(f'Wrote endpoint "{name}" which consists of {len(required_types)} nested model class(es)')

try:
  endpoints = { n: types[n].clone_exclude(fields) for n, *fields in args.endpoint_exclude_fields } | { n: types[n].clone_include(fields) for n, *fields in args.endpoint_include_fields }

  # write to files or stdout
  for name, endpoint_types in endpoints.items():
    write_endpoint(name, endpoint_types)

except RuntimeError as e:
  logger.error(e)
  sys.exit(1)
