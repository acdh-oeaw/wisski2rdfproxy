from wisskas.model import write_model

import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--input", type=argparse.FileType("r"), help="a WissKI pathbuilder file"
)
parser.add_argument("--output", type=str, help="output filename")

args = parser.parse_args()

print(
    write_model(
        {
            "classes": {
                "DummyOne": {
                    "fields": {
                        "foo": {"type": "str"},
                        "bar": {"type": "str", "binding": "yadda"},
                    }
                }
            }
        }
    )
)
