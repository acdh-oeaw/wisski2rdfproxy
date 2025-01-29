from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(loader=PackageLoader("wisskas"), autoescape=select_autoescape())


def write_model(*args):
    template = env.get_template("model.jinja2")
    return template.render(*args)
