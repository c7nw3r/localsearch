import json
import os
from pathlib import Path


def write_json(path: str, document: dict, indent=None):
    if not os.path.exists(Path(path).parent):
        os.makedirs(Path(path).parent)

    with open(path, "w") as f:
        f.write(json.dumps(document, indent=indent))


def read_json(path: str):
    with open(path, "r") as f:
        return json.load(f)
