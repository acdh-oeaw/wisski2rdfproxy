from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(loader=PackageLoader("wisskas"), autoescape=select_autoescape())


def serialize(template_name, **kwargs):
    template = env.get_template(f"{template_name}.jinja2")
    return template.render(**kwargs)


def serialize_model(root):
    return serialize("model", **{"root": root})


def serialize_query(root, prefixes={}):
    return serialize("query", **{"root": root, "prefixes": prefixes})
