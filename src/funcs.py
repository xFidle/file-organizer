import fnmatch

from commands import chmod_file, copy_file, remove_file, rename_file
from utils import Kind, ask_user, find_new_name, get_hash, print_instruction


def handle_copy(all_files, X, exec_mode):
    to_copy = [entry for entry in all_files.values() if entry.kind == Kind.Y and not (X / entry.rel).exists()]
    print("Found {} files which has no corresponding file in X!".format(len(to_copy)))
    return _interactive_pipeline(to_copy, lambda x, m: copy_file(x.path, X / x.rel, X, Kind.X, m), "Copy", exec_mode)


def handle_same_names(all_files, exec_mode):
    files_by_name = {}
    for entry in all_files.values():
        files_by_name.setdefault(entry.name, []).append(entry)
    print("Found {} files with same names in total!\n".format(sum(len(x) - 1 for x in files_by_name.values())))

    removed = []
    for _, group in files_by_name.items():
        if len(group) < 2:
            continue
        group.sort(key=lambda x: x.m_time, reverse=True)
        to_keep, to_remove = group[0], group[1:]
        print("File to keep (newest) {}".format(to_keep.path))
        print("Found {} files wish same names".format(len(to_remove)))
        r = _interactive_pipeline(to_remove, remove_file, "Delete", exec_mode)
        removed.extend(r)

    return removed


def handle_duplicates(all_files, exec_mode):
    files_by_hash = {}
    for entry in all_files.values():
        if entry.size == 0:
            continue
        hash = get_hash(entry.path)
        files_by_hash.setdefault(hash, []).append(entry)
    print("Found {} duplicates in total!\n".format(sum(len(x) - 1 for x in files_by_hash.values() if len(x) > 1)))

    removed = []
    for hash, group in files_by_hash.items():
        if len(group) < 2:
            continue
        group.sort(key=lambda x: x.m_time)
        to_keep, to_remove = group[0], group[1:]
        print("File to KEEP (oldest) {}".format(to_keep.path))
        print("Found {} file duplicate(s)".format(len(to_remove)))
        r = _interactive_pipeline(to_remove, remove_file, "Delete", exec_mode)
        removed.extend(r)

    return removed


def handle_permissions(file_entries, mode, exec_mode):
    invalid_files = [entry for entry in file_entries.values() if entry.mode != mode]
    print("Found {} file(s) with invalid permissions.".format(len(invalid_files)))
    return _interactive_pipeline(invalid_files, lambda x, m: chmod_file(x, mode, m), "CHMOD", exec_mode)


def handle_messy_files(file_entries, messy_chars, substitute, exec_mode):
    messy_files = [entry for entry in file_entries.values() if any(c in messy_chars for c in entry.name)]
    print("Found {} messy file(s)".format(len(messy_files)))
    return _interactive_pipeline(
        messy_files,
        lambda x, m: rename_file(x, find_new_name(x, messy_chars, substitute), m),
        "Sanitize (replace messy chars with '{}')".format(substitute),
        exec_mode,
    )


def handle_temporary_files(file_entries, patterns, exec_mode):
    temporary_files = [
        entry for entry in file_entries.values() if any(fnmatch.fnmatch(entry.name, p) for p in patterns)
    ]
    print("Found {} temporary file(s).".format(len(temporary_files)))
    return _interactive_pipeline(temporary_files, remove_file, "Delete", exec_mode)


def handle_empty_files(file_entries, exec_mode):
    empty_files = [entry for entry in file_entries.values() if entry.size == 0]
    print("Found {} empty file(s).".format(len(empty_files)))
    return _interactive_pipeline(empty_files, remove_file, "Delete", exec_mode)


def _interactive_pipeline(entries, fn, action, exec_mode):
    if not entries:
        return []

    n = len(entries)
    inst = {
        "y": "{} all files".format(action),
        "N": "Do nothing",
        "i": "Inspect files one by one",
        "p": "Print found files",
        "q": "Quit",
    }

    print_instruction(inst)
    while True:
        answer = ask_user("What would you like to do?", list(inst.keys()), exec_mode)
        if answer != "p":
            break
        for entry in entries:
            print("-> File: {}".format(entry.path))

    if answer == "q":
        return []

    changes = []

    if answer == "y":
        for entry in entries:
            changes.append(fn(entry.path, exec_mode))

    if answer == "i":
        for i, entry in enumerate(entries):
            answer = ask_user(
                "[{}/{}] File: {} {}? [y, N, q]".format(i + 1, n, entry.path, action),
                ["y", "N", "q"],
                exec_mode,
            )
            if answer == "y":
                changes.append(fn(entry.path, exec_mode))

            if answer == "q":
                break

    return changes
