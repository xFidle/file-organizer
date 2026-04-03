import fnmatch
import stat

from commands import chmod_file, remove_file, rename_file
from utils import ask_user, find_new_name, get_hash, print_instruction


def handle_duplicates(files):
    files_by_hash = {}
    for f in files:
        if f.stat().st_size < 0:
            continue
        hash = get_hash(f)
        files_by_hash.setdefault(hash, []).append(f)

    removed = []

    if all(len(x) == 1 for x in files_by_hash.values()):
        print("Found 0 duplicates in total.")

    for file_hash, files in files_by_hash.items():
        if len(files) < 2:
            continue

        files.sort(key=lambda f: f.stat().st_mtime)
        oldest = files[0]
        to_delete = files[1:]

        print("Found {} duplicate(s) of {} which are not empty.".format(len(to_delete), oldest))
        r = _single_pipeline(to_delete, remove_file, "Delete")
        removed.extend(r)

    return removed


def handle_missing_files(files):
    pass


def handle_permissions(files, mode):
    invalid_files = [f for f in files if stat.S_IMODE(f.stat().st_mode) != mode]

    print("Found {} file(s) with invalid permissions.".format(len(invalid_files)))

    if not invalid_files:
        return

    _ = _single_pipeline(invalid_files, lambda f: chmod_file(f, mode), "CHMOD")


def handle_messy_files(files, messy_chars, substitute):
    messy_files = [f for f in files if any(c in messy_chars for c in str(f))]

    print("Found {} messy file(s)".format(len(messy_files)))

    if not messy_files:
        return []

    return _single_pipeline(
        messy_files,
        lambda f: rename_file(f, find_new_name(f, messy_chars, substitute)),
        "Sanitize (replace messy chars with '{}')".format(substitute),
    )


def handle_temporary_files(files, patterns):
    temporary_files = [f for f in files if any(fnmatch.fnmatch(str(f), p) for p in patterns)]

    print("Found {} temporary file(s).".format(len(temporary_files)))

    if not temporary_files:
        return []

    return _single_pipeline(temporary_files, remove_file, "Delete")


def handle_empty_files(files):
    empty_files = [f for f in files if f.stat().st_size == 0]

    print("Found {} empty file(s).".format(len(empty_files)))

    if not empty_files:
        return []

    return _single_pipeline(empty_files, remove_file, "Delete")


def _single_pipeline(found_files, fn, action):
    n = len(found_files)
    inst = {
        "y": "{} all files".format(action),
        "N": "Do nothing",
        "i": "Inspect files one by one",
        "p": "Print found files",
        "q": "Quit",
    }

    print_instruction(inst)
    while True:
        answer = ask_user("What would you like to do?", list(inst.keys()))
        if answer != "p":
            break
        for fpath in found_files:
            print("-> File: {}".format(fpath))

    if answer == "q":
        return []

    changes = []

    if answer == "y":
        for i, fpath in enumerate(found_files):
            result = fn(fpath)
            if result is not None:
                changes.append(result)

    if answer == "i":
        for i, fpath in enumerate(found_files):
            answer = ask_user("[{}/{}] File: {} {}? [y, N, q]".format(i + 1, n, fpath, action), ["y", "N", "q"])
            if answer == "y":
                result = fn(fpath)
                if result is not None:
                    changes.append(result)

            if answer == "q":
                break

    return changes
