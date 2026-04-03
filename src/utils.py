import hashlib
import os
from pathlib import Path


def ask_user(prompt, options):
    while True:
        answer = input(prompt + " ")
        if answer.strip() in options:
            return answer


def print_instruction(instruction):
    for key, info in instruction.items():
        print("[{}] {}".format(key, info))


def collect_files(directories):
    result: set[Path] = set()
    for dir in directories:
        for root, _, files in os.walk(dir, topdown=True):
            for fname in files:
                full_path = Path(root) / fname
                if full_path.is_file():
                    result.add(full_path)
    return result


def get_hash(fpath, block_size=1 << 16):
    sha256 = hashlib.sha256()
    with open(fpath, "rb") as f:
        for block in iter(lambda: f.read(block_size), b""):
            sha256.update(block)
    return sha256.hexdigest()


def get_home_path():
    home = os.path.expanduser("~")
    if not home or home == "~":
        home = os.environ.get("HOME") or "/"
    return Path(home)


def find_new_name(fpath, messy_chars, substitute):
    f = str(fpath)
    for ch in messy_chars:
        f = f.replace(ch, substitute)

    new_fpath = Path(f)
    if not new_fpath.exists():
        return new_fpath

    parent = new_fpath.parent
    stem = new_fpath.stem
    suffix = new_fpath.suffix
    i = 1
    while True:
        new_fpath = parent / "{}_{}{}".format(stem, i, suffix)
        if not new_fpath.exists():
            break

        i += 1

    return new_fpath
