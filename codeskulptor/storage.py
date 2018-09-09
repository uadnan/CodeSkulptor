import os
from pathlib import Path

BASE_DIR = os.path.join(Path.home(), ".codeskulptor", "storage")


def abs_path(path):
    return os.path.join(BASE_DIR, path)


def file_exists(path):
    return os.path.exists(abs_path(path))


def save_file(path, content):
    os.makedirs(BASE_DIR, exist_ok=True)

    with open(abs_path(path), "w") as f:
        f.write(content)
