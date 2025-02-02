FILTER_PATH_SEPARATOR = "."
FILTER_PATH_INVERSION = "^"


def create_names(
    prefix: str | list[str], postfix: str, used_names=set(), n=1
) -> list[str]:
    # TODO check if already in used_names
    return (
        []
        if n == 0
        else [*(f"{prefix}_{i}_{postfix}" for i in range(n - 1)), f"{prefix}_{postfix}"]
    )


def id_to_classname(path_id) -> str:
    return path_id.replace("_", " ").title().replace(" ", "")


def parse_endpointspec(pathid_endpointname) -> tuple[str, str]:
    if "/" in pathid_endpointname:
        return pathid_endpointname.split("/", 1)
    else:
        return (pathid_endpointname, pathid_endpointname)


def parse_filterspec(filterspec):
    split = [i.split(FILTER_PATH_SEPARATOR, 1) for i in filterspec]
    prefixes = set(p for p, *_r in split)
    return {p: [r[1] for r in split if r[0] == p and len(r) > 1] for p in prefixes}


def path_to_camelcase(path):
    # or .title() on spaced string
    return "".join([s.capitalize() for s in split_path(path)])


def split_path(path):
    return path.lstrip("/").split("/")
