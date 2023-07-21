import json
import os
from pathlib import Path
from typing import List


def read_json(path: str) -> dict:
    with open(path, "r") as f:
        import json
        return json.loads(f.read())


def read_json_lines(path: str) -> List[dict]:
    with open(path, "r") as f:
        import json
        return list(map(lambda x: json.loads(x), f.readlines()))


def write_json(path: str, document: dict, indent=None):
    if not os.path.exists(Path(path).parent):
        os.makedirs(Path(path).parent)

    with open(path, "w") as f:
        f.write(json.dumps(document, indent=indent))
