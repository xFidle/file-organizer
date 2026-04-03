import fnmatch

from commands import chmod_file, move_file_safely, remove_file, rename_file
from utils import X_KIND, ask_user, find_new_name, get_hash, print_instruction


def handle_duplicates(group, X, fallback_dir):
    files_by_hash = {}
    for f in group:
        if f["size"] == 0:
            continue
        hash = get_hash(f["path"])
        files_by_hash.setdefault(hash, []).append(f)

    print("Found {} duplicates in total.".format(sum(len(x) - 1 for x in files_by_hash.values() if len(x) > 1)))

    removed = []

    for hash, group in files_by_hash.items():
        if len(group) < 2:
            continue

        group.sort(key=lambda f: f["m_time"])

        to_keep = None
        for f in group:
            if f["kind"] == X_KIND:
                to_keep = f
                break
        else:
            to_keep = group[0]

        to_remove = [f for f in group if f is not to_keep]

        if to_keep["kind"] != X_KIND:
            print("WARNING: File to KEEP is not from 'X'!")
        print("File to KEEP {}".format(to_keep["path"]))
        print("Found {} file duplicate(s)".format(len(to_remove)))

        r = _interactive_pipeline(
            to_remove,
            lambda x: remove_file(x["path"]),
            "Delete",
            prehook=lambda: _duplicates_prehook(to_keep, X, fallback_dir),
        )
        removed.extend(r)

    return removed


def _duplicates_prehook(to_keep, X, fallback_dir):
    if to_keep["kind"] == X_KIND:
        return True

    answer = ask_user(
        "Move selected file to X? [y, N, q]",
        ["y", "N", "q"],
    )
    if answer == "y":
        res = move_file_safely(
            to_keep["path"],
            X / to_keep["rel"],
            fallback_dir,
        )
        if res is None:
            return False

        if res is not None and not res.get("skipped", False):
            # TODO: Update file entry
            pass

        return True

    elif answer in ("N", "q"):
        return True


def handle_permissions(file_entries, mode):
    invalid_files = [entry for entry in file_entries if entry["mode"] != mode]

    print("Found {} file(s) with invalid permissions.".format(len(invalid_files)))

    if not invalid_files:
        return

    return _interactive_pipeline(invalid_files, lambda x: chmod_file(x["path"], mode), "CHMOD")


def handle_messy_files(file_entries, messy_chars, substitute):
    messy_files = [entry for entry in file_entries if any(c in messy_chars for c in entry["name"])]

    print("Found {} messy file(s)".format(len(messy_files)))

    if not messy_files:
        return []

    return _interactive_pipeline(
        messy_files,
        lambda x: rename_file(x["path"], find_new_name(x["path"], messy_chars, substitute)),
        "Sanitize (replace messy chars with '{}')".format(substitute),
    )


def handle_temporary_files(file_entries, patterns):
    temporary_files = [entry for entry in file_entries if any(fnmatch.fnmatch(entry["name"], p) for p in patterns)]

    print("Found {} temporary file(s).".format(len(temporary_files)))

    if not temporary_files:
        return []

    return _interactive_pipeline(temporary_files, lambda x: remove_file(x["path"]), "Delete")


def handle_empty_files(file_entries):
    empty_files = [entry for entry in file_entries if entry["size"] == 0]

    print("Found {} empty file(s).".format(len(empty_files)))

    if not empty_files:
        return []

    return _interactive_pipeline(empty_files, lambda x: remove_file(x["path"]), "Delete")


def _interactive_pipeline(found_entries, fn, action, prehook=None):
    if prehook is not None and not prehook():
        return []

    n = len(found_entries)
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
        for entry in found_entries:
            print("-> File: {}".format(entry["path"]))

    if answer == "q":
        return []

    changes = []

    if answer == "y":
        for entry in found_entries:
            result = fn(entry)
            if result is not None:
                changes.append(result)

    if answer == "i":
        for i, entry in enumerate(found_entries):
            answer = ask_user(
                "[{}/{}] File: {} {}? [y, N, q]".format(i + 1, n, entry["path"], action),
                ["y", "N", "q"],
            )
            if answer == "y":
                result = fn(entry)
                if result is not None:
                    changes.append(result)

            if answer == "q":
                break

    return changes
