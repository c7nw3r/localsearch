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


def grep(folder: str, prefix: str):
    for root, _, files in os.walk(folder):
        for file in files:
            if file.startswith(prefix):
                return f"{root}/{file}"

    print(f"no file found in folder {folder} with prefix {prefix}")
    return None


def list_files(path: str, recursive: bool = False):
    if not recursive:
        return os.listdir(path)
    all_files = []
    for _, _, files in os.walk(path):
        all_files.extend(files)
    return all_files


def delete_file(path: str):
    try:
        os.remove(path)
    except:
        print(f"error while deleting file {path}")


def delete_folder(path: str):
    import shutil
    shutil.rmtree(path)
