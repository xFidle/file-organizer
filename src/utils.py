import hashlib
import os
import stat
from pathlib import Path

X_KIND = "X"
Y_KIND = "Y"


def ask_user(prompt, options):
    while True:
        answer = input(prompt + " ")
        if answer.strip() in options:
            return answer


def print_instruction(instruction):
    for key, info in instruction.items():
        print("[{}] {}".format(key, info))


def collect_files(X, Y_dirs):
    result = []

    scan_roots = [(X, X_KIND)]
    scan_roots.extend([(Y, Y_KIND) for Y in Y_dirs])

    for root, root_kind in scan_roots:
        for walk_dir, _, files in os.walk(root, topdown=True):
            for fname in files:
                full_path = Path(walk_dir) / fname
                if not full_path.is_file():
                    continue

                try:
                    st = full_path.stat()
                except OSError:
                    continue

                entry = {
                    "path": full_path,
                    "root": root,
                    "kind": root_kind,
                    "rel": full_path.relative_to(root),
                    "name": full_path.name,
                    "size": st.st_size,
                    "m_time": st.st_mtime,
                    "mode": stat.S_IMODE(st.st_mode),
                }

                result.append(entry)

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
    return generate_unique_path(new_fpath)


def generate_unique_path(fpath):
    if not fpath.exists():
        return fpath

    parent = fpath.parent
    stem = fpath.stem
    suffix = fpath.suffix
    i = 1
    while True:
        new_fpath = parent / "{}_{}{}".format(stem, i, suffix)
        if not new_fpath.exists():
            break

        i += 1

    return new_fpath
