FILTER_PATH_SEPARATOR = ">"
FILTER_PATH_INVERSION = "^"


def create_names(prefix, postfix, used_names=[], n=1):
    # TODO check if already in used_names
    return f"{prefix}_{postfix}"


def id_to_classname(path_id):
    return path_id.replace("_", " ").title().replace(" ", "")


def parse_filter_list(ls):
    split = [i.split(FILTER_PATH_SEPARATOR, 1) for i in ls]
    prefixes = set(p for p, *_r in split)
    return {p: [r[1] for r in split if r[0] == p and len(r) > 1] for p in prefixes}


def path_to_camelcase(path):
    # or .title() on spaced string
    return "".join([s.capitalize() for s in split_path(path)])


def split_path(path):
    return path.lstrip("/").split("/")
