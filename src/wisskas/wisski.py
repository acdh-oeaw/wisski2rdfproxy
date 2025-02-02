import logging
from lxml import objectify
from wisskas.string_utils import id_to_classname

WISSKI_TYPES = {
    # TODO add support for all Wisski field types: https://wiss-ki.eu/documentation/pathbuilder/configuration/lists
    "string": "str",
    "list_string": "list[str]",  # FIXME this doesn't get annotated properly, need to change the Type's cardinality instead
    "uri": "AnyUrl",
}


def parse_path(path_element):
    properties = {child.tag: child for child in path_element.iterchildren()}
    properties["path_array"] = [
        el.text for el in path_element.path_array.iterchildren()
    ]
    if properties["datatype_property"] == "empty":
        properties["datatype_property"] = None

    properties["fields"] = {}
    properties["parents"] = {}

    if properties["fieldtype"] and properties["fieldtype"] != "entity_reference":
        # set python field type
        properties["type"] = WISSKI_TYPES[properties["fieldtype"]]

    if properties["is_group"]:
        properties["class_name"] = id_to_classname(str(properties["id"]))

    if properties["group_id"] == 0:
        # this is a root type
        properties["rdf_class"] = properties["path_array"][-1]

    return (path_element.id, properties)


def root_type_dict(paths: list[dict]):
    # create rdf class to type mapping
    return {path["rdf_class"]: path for path in paths if "rdf_class" in path}


def parse_flat_paths(file):
    # parse flat list of paths
    return dict(
        parse_path(path)
        for path in objectify.parse(file).getroot().iterchildren()
        if path.enabled
    )


def nest_paths(paths):
    root_types = root_type_dict(paths.values())

    # create nested structure
    for path in paths.values():
        if path["group_id"]:
            paths[path["group_id"]]["fields"][path["id"]] = path
            if path["fieldtype"] == "entity_reference":
                # look up based on CRM type
                try:
                    path["reference"] = root_types[path["path_array"][-1]]
                    path["reference"]["parents"][path["id"]] = path
                    # path["fields"] = path["reference"]["fields"]
                    # path["is_group"] = 1
                except KeyError as e:
                    logging.warning(
                        f"path {path['id']} is an entity_reference, but no known path for target CRM class {e}"
                    )
    return (root_types, paths)


def parse_paths(file):
    return nest_paths(parse_flat_paths(file))
