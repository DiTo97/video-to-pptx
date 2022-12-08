import argparse
import pathlib
import re
import typing
from typing import Any


def parse_args() -> typing.Dict[str, Any]:
    parser = argparse.ArgumentParser()

    parser.add_argument("filepath")
    parser.add_argument("pattern")
    parser.add_argument("replacement")

    namespace = parser.parse_args()
    return vars(namespace)


def replace(filepath: str, pattern: str, replacement: str) -> None:
    """It replaces matches of the given pattern in the file with the given path"""
    filepath = pathlib.Path(filepath).resolve()

    if not filepath.exists():
        raise FileNotFoundError(str(filepath))

    with filepath.open("rt") as f:
        contents = f.read()

    contents = re.sub(pattern, replacement, contents)

    with filepath.open("wt") as f:
        f.write(contents)


if __name__ == "__main__":
    args = parse_args()
    replace(**args)
