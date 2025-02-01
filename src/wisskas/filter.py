import copy
import logging

from wisskas.string_utils import (
    FILTER_PATH_SEPARATOR,
    parse_filterspec,
)
from wisskas.wisski import WISSKI_TYPES


def handle_recursion(prefix):
    # TODO try to find recursion pattern === identical adjacent sequences of path ids
    raise RuntimeError("recursion somewhere")


def create_clone(element, filterspec, prefix=[]):
    # shallow copy
    clone = copy.copy(element)
    filters = parse_filterspec(filterspec)
    for key in filters:
        if key == "*" or key == "**":
            if key == "*" and len(clone["fields"]) == 0:
                logging.warning(
                    f"found '{key}' at {'.'.join(prefix[1:])} even though there are no fields"
                )
            else:
                logging.debug(f"clone: found '{key}' in type '{clone}'")
            continue
        exists = False
        # TODO strip/handle inversion marker
        for f in clone["fields"].values():
            if f["id"] == key:
                logging.debug(f"clone: found '{key}' in field of '{clone['id']}'")
                exists = True
                break
        if not exists:
            logging.warning(
                f"unknown field specified in include/exclude list at {FILTER_PATH_SEPARATOR.join(prefix[1:])}: {key}"
            )
    return (clone, filters)


def clone_exclude(element, exclude, prefix=[], used_names=[]):
    print(element["id"])
    print(prefix)
    clone, excludes = create_clone(element, exclude, prefix)
    if "*" in exclude:
        logging.debug("all fields of this should be excluded")
        clone["type"] = WISSKI_TYPES["uri"]
        # clone.datatype_property = None
        return clone
    try:
        # FIXME handle entity_reference
        clone["fields"] = {
            name: clone_exclude(f, excludes.get(f["id"], []), prefix)
            for name, f in clone["fields"].items()
            if excludes.get(f["id"], None) != []
        }
    except RecursionError:
        handle_recursion(prefix)
    return clone


def clone_include(element, include, prefix=[], used_names=[]):
    clone, includes = create_clone(element, include, prefix)
    return clone
