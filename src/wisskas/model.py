# type: ignore
from pathlib import Path
from datamodel_code_generator import InputFileType, generate
from importlib.resources import files


def write_model(schema, path: Path):
    generate(
        schema,
        input_file_type=InputFileType.JsonSchema,
        output=path,
        field_include_all_keys=True,
        custom_template_dir=files("wisskas.templates"),
    )
    return path.read_text()
