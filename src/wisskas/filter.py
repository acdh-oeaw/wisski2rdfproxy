import copy
import logging

from wisskas.string_utils import (
    FILTER_PATH_SEPARATOR,
    create_names,
    parse_filterspec,
)
from wisskas.wisski import WISSKI_TYPES


def endpoint_exclude_fields(root, exclude, root_classname=None):
    # TODO create dummy root class
    dummy = {"path_array": [], "fields": {root_classname: root}}
    return clone_exclude(dummy, root_classname, exclude)


def endpoint_include_fields(root, include, root_classname=None):
    # TODO create dummy root class
    dummy = {"path_array": [], "fields": {root_classname: root}}
    return clone_exclude(dummy, root_classname, include)


def handle_recursion(prefix):
    # TODO try to find recursion pattern === identical adjacent sequences of path ids
    raise RuntimeError("recursion somewhere")


def create_clone(parent, fieldname, filterspec, prefix, used_names):
    # shallow copy
    clone = copy.copy(parent["fields"][fieldname])

    varnames = [] if "binding_vars" in parent else [fieldname]

    if clone["fieldtype"] == "entity_reference":
        logging.debug(f"cloning reference to '{clone['reference']['id']}'")
        # TODO handle entity_reference
        # clone["fields"] = clone["reference"]["fields"]
        pass
    else:
        for a, b in zip(parent["path_array"], clone["path_array"]):
            if a == b:
                logging.debug(
                    f"ignoring prefix {a} in '{clone['id']}' because it exists in parent '{parent['id']}'"
                )
                varnames.append(None)
            else:
                break
        if clone["datatype_property"]:
            clone["path_array"].append(clone["datatype_property"])

    if "binding_vars" in parent:
        varnames.append(parent["binding_vars"][-1])

        for name in create_names(
            varnames[-1] if varnames else "",
            clone["id"],
            used_names,
            1 + (len(clone["path_array"]) - len(varnames)) // 2,
        ):
            varnames.append(name)
            varnames.append(name)

    clone["binding_vars"] = varnames
    clone["binding"] = varnames[-1]

    logging.debug(
        f"cloning {fieldname} (path id {clone['id']}, prefix {prefix}) with binding vars: {clone['binding_vars']}"
    )
    filters = parse_filterspec(filterspec)
    for key in filters:
        if key == "*" or key == "**":
            if key == "*" and len(clone["fields"]) == 0:
                logging.warning(
                    f"found '{key}' at {'.'.join(prefix[1:])} even though there are no fields"
                )
            else:
                logging.debug(f"clone: found '{key}' in type '{clone['id']}'")
            continue
        exists = False
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


def clone_exclude(parent, fieldname, exclude, prefix=[], used_names=set()):
    clone, excludes = create_clone(parent, fieldname, exclude, prefix, used_names)
    # TODO set binding_var and path_vars
    if "*" in exclude:
        logging.debug("all fields of this should be excluded")
        clone["type"] = WISSKI_TYPES["uri"]
        clone["fields"] = {}
        # clone.datatype_property = None
        return clone
    try:
        clone["fields"] = {
            name: clone_exclude(clone, name, excludes.get(f["id"], []), prefix)
            for name, f in clone["fields"].items()
            if excludes.get(f["id"], None) != []
        }
    except RecursionError:
        handle_recursion(prefix)
    return clone


def clone_include(parent, fieldname, include, prefix=[], used_names=set()):
    clone, includes = create_clone(parent, fieldname, include, prefix, used_names)
    return clone
