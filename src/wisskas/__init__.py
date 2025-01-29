from pathlib import Path
from wisskas.model import write_model


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input", type=argparse.FileType("r"), help="a WissKI pathbuilder file"
    )
    parser.add_argument("output", type=str, help="output filename")

    args = parser.parse_args()

    print(
        write_model(
            # dummy schema
            """
            {
            "title": "Dummy",
            "type": "object",
            "properties":
                {"a":
                    {
                    "type":"string"
                    }
                }
            }""",
            Path(args.output),
        )
    )


if __name__ == "__main__":
    main()
