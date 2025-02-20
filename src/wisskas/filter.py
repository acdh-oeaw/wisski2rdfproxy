import copy
import logging

from wisskas.string_utils import (
    FILTER_PATH_SEPARATOR,
    create_names,
    parse_filterspec,
)
from wisskas.wisski import WISSKI_TYPES


class DummyRootPath:
    def __init__(self, root_classname, root):
        self.path_array = []
        self.binding_vars = []
        self.fields = {root_classname: root}


def endpoint_exclude_fields(root, exclude, root_classname=None):
    return clone_exclude(DummyRootPath(root_classname, root), root_classname, exclude)


def endpoint_include_fields(root, include, root_classname=None):
    return clone_include(DummyRootPath(root_classname, root), root_classname, include)


def handle_recursion(prefix):
    # TODO try to find recursion pattern === identical adjacent sequences of path ids
    raise RuntimeError("recursion somewhere")


def debug(task, path, msg, depth):
    logging.debug(f"{' ' * 2 * depth}{task} {path.id}: {msg}")


def debug_clone(path, msg, depth=0):
    debug("cloning", path, msg, depth)


def debug_filter(path, msg, depth=0):
    debug("filtering", path, msg, depth)


def create_clone(parent, fieldname, filterspec, prefix, used_names, depth=0):
    # shallow copy
    clone = copy.copy(parent.fields[fieldname])
    clone.path_array = copy.copy(clone.path_array)

    if parent.path_array == []:
        debug_clone(
            clone,
            f"root type, changing classname from {clone.class_name} to {fieldname}",
        )
        clone.class_name = fieldname
        clone.root = True

    varnames = copy.copy(parent.binding_vars) if parent.binding_vars else [fieldname]

    if clone.entity_reference:
        debug_clone(clone, f"entity reference to '{clone.entity_reference.id}'", depth)
        clone.fields = clone.reference.fields
        clone.class_name = f"{parent.class_name}_{clone.entity_reference.class_name}"
        clone.name = clone.reference.name
    # set parent paths to None
    if len(clone.path_array) > len(parent.path_array):
        for i in range(len(parent.path_array)):
            if (
                parent.path_array[i] is None
                or clone.path_array[i] == parent.path_array[i]
            ):
                debug_clone(
                    clone,
                    f"ignoring prefix because it exists in parent '{parent.id}'",
                    depth,
                )
                clone.path_array[i] = None
            else:
                break
    else:
        # child of an entity_reference
        varnames = [parent.binding_vars[-1]]
        clone.path_array[0] = None

    if clone.datatype_property:
        debug_clone(clone, f"adding datatype_property to {clone.path_array}")
        clone.path_array.append(clone.datatype_property)

    if parent.binding_vars:
        for name in create_names(
            varnames[-1] if varnames else "",
            clone.id,
            used_names,
            1 + len(clone.path_array) // 2 - len(varnames),
        ):
            varnames.append(name)

    clone.binding_vars = varnames
    clone.binding = varnames[-1]
    debug_clone(clone, f"path {clone.path_array}", depth)
    debug_clone(clone, f"binding vars {clone.binding_vars}", depth)

    filters = parse_filterspec(filterspec)
    for key in filters:
        if key == "*" or key == "**":
            if key == "*" and len(clone["fields"]) == 0:
                logging.warning(
                    f"found '{key}' at {'.'.join(prefix[1:])} even though there are no fields"
                )
            else:
                debug_clone(clone, f"found field '{key}'", depth)
            continue
        exists = False
        for f in clone["fields"].values():
            if f["id"] == key:
                debug_clone(clone, f"found field '{key}'", depth)
                exists = True
                break
        if not exists:
            logging.warning(
                f"cloning {clone.id} unknown field specified in include/exclude list at {FILTER_PATH_SEPARATOR.join(prefix[1:])}: {key}"
            )
    return (clone, filters)


def clone_exclude(parent, fieldname, exclude, prefix=[], used_names=set(), depth=0):
    clone, excludes = create_clone(
        parent, fieldname, exclude, prefix, used_names, depth
    )
    debug_filter(clone, f"exclude {excludes}")
    if "*" in exclude:
        clone.type = WISSKI_TYPES["uri"]
        clone.fields = {}
        # clone.datatype_property = None
        return clone
    try:
        clone.fields = {
            name: clone_exclude(
                clone, name, excludes.get(f.id, []), prefix, used_names, depth + 1
            )
            for name, f in clone.fields.items()
            if excludes.get(f.id, None) != []
        }
    except RecursionError:
        handle_recursion(prefix)
    return clone


def clone_include(parent, fieldname, include, prefix=[], used_names=set(), depth=0):
    clone, includes = create_clone(
        parent, fieldname, include, prefix, used_names, depth
    )
    debug_filter(clone, f"include {includes}", depth)
    if "**" in include:
        clone.fields = {
            name: clone_include(clone, name, ["**"], prefix, used_names)
            for name in clone.fields.keys()
        }
    else:
        clone["fields"] = {
            name: clone_include(
                clone, name, includes.get(name, []), prefix, used_names, depth + 1
            )
            for name in clone["fields"].keys()
            if "*" in include or name in includes
        }
    if len(clone["fields"]) == 0 and not clone["datatype_property"]:
        debug_filter(clone, "class is down to 0 fields", depth)
        clone["type"] = WISSKI_TYPES["uri"]
    else:
        debug_filter(clone, f"remaining fields {list(clone['fields'].keys())}", depth)
    return clone
