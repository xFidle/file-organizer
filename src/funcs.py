import fnmatch

from commands import apply_moved, chmod_file, move_file_safely, remove_file, rename_file
from utils import X_KIND, ask_user, find_new_name, get_hash, print_instruction


def handle_duplicates(all_files, X, fallback_dir, auto_accept):
    files_by_hash = {}
    for entry in all_files.values():
        if entry.size == 0:
            continue
        hash = get_hash(entry.path)
        files_by_hash.setdefault(hash, []).append(entry)

    print("Found {} duplicates in total.".format(sum(len(x) - 1 for x in files_by_hash.values() if len(x) > 1)))

    removed = []

    for hash, group in files_by_hash.items():
        if len(group) < 2:
            continue

        group.sort(key=lambda x: x.m_time)

        to_keep = None
        for entry in group:
            if entry.kind == X_KIND:
                to_keep = entry
                break
        else:
            to_keep = group[0]

        to_remove = [entry.path for entry in group if entry is not to_keep]

        if to_keep.kind != X_KIND:
            print("WARNING: File to KEEP is not from 'X'!")
        print("File to KEEP {}".format(to_keep.path))
        print("Found {} file duplicate(s)".format(len(to_remove)))

        r = _interactive_pipeline(
            to_remove,
            remove_file,
            "Delete",
            auto_accept,
            prehook=lambda: _duplicates_prehook(to_keep, X, fallback_dir, auto_accept, all_files),
        )
        removed.extend(r)

    return removed


def _duplicates_prehook(to_keep, X, fallback_dir, auto_accept, all_files):
    if to_keep.kind == X_KIND:
        return True

    answer = ask_user("Move selected file to X? [y, N, q]", ["y", "N", "q"], auto_accept)
    if answer == "y":
        try:
            res = move_file_safely(
                to_keep.path,
                X / to_keep.rel,
                fallback_dir,
                new_root=X,
                new_kind=X_KIND,
            )
        except OSError as e:
            print("-> Error: {}".format(e))
            return False

        if res is not None:
            apply_moved(all_files, [res])

        return True

    elif answer in ("N", "q"):
        return True


def handle_permissions(file_entries, mode, auto_accept):
    invalid_files = [path for path, entry in file_entries.items() if entry.mode != mode]

    print("Found {} file(s) with invalid permissions.".format(len(invalid_files)))

    return _interactive_pipeline(invalid_files, lambda x: chmod_file(x, mode), "CHMOD", auto_accept)


def handle_messy_files(file_entries, messy_chars, substitute, auto_accept):
    messy_files = [path for path, entry in file_entries.items() if any(c in messy_chars for c in entry.name)]

    print("Found {} messy file(s)".format(len(messy_files)))

    return _interactive_pipeline(
        messy_files,
        lambda x: rename_file(x, find_new_name(x, messy_chars, substitute)),
        "Sanitize (replace messy chars with '{}')".format(substitute),
        auto_accept,
    )


def handle_temporary_files(file_entries, patterns, auto_accept):
    temporary_files = [
        path for path, entry in file_entries.items() if any(fnmatch.fnmatch(entry.name, p) for p in patterns)
    ]

    print("Found {} temporary file(s).".format(len(temporary_files)))

    return _interactive_pipeline(temporary_files, remove_file, "Delete", auto_accept)


def handle_empty_files(file_entries, auto_accept):
    empty_files = [path for path, entry in file_entries.items() if entry.size == 0]

    print("Found {} empty file(s).".format(len(empty_files)))

    return _interactive_pipeline(empty_files, remove_file, "Delete", auto_accept)


def _interactive_pipeline(paths, fn, action, auto_accept, prehook=None):
    if not paths:
        return []

    if prehook is not None and not prehook():
        return []

    n = len(paths)
    inst = {
        "y": "{} all files".format(action),
        "N": "Do nothing",
        "i": "Inspect files one by one",
        "p": "Print found files",
        "q": "Quit",
    }

    print_instruction(inst)
    while True:
        answer = ask_user("What would you like to do?", list(inst.keys()), auto_accept)
        if answer != "p":
            break
        for path in paths:
            print("-> File: {}".format(path))

    if answer == "q":
        return []

    changes = []

    if answer == "y":
        for path in paths:
            try:
                changes.append(fn(path))
            except OSError as e:
                print("-> Error: {}".format(e))

    if answer == "i":
        for i, path in enumerate(paths):
            answer = ask_user(
                "[{}/{}] File: {} {}? [y, N, q]".format(i + 1, n, path, action),
                ["y", "N", "q"],
                auto_accept,
            )
            if answer == "y":
                try:
                    changes.append(fn(path))
                except OSError as e:
                    print("-> Error: {}".format(e))

            if answer == "q":
                break

    return changes
