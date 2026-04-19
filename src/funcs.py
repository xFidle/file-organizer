import fnmatch

from commands import chmod_file, copy_file, remove_file, rename_file
from utils import X_KIND, Y_KIND, ask_user, find_new_name, get_hash, print_instruction


def handle_copy(all_files, X, auto_accept):
    to_copy = [entry for entry in all_files.values() if entry.kind == Y_KIND and not (X / entry.rel).exists()]
    print("Found {} files which has no corresponding file in X!".format(len(to_copy)))
    return _interactive_pipeline(to_copy, lambda x: copy_file(x.path, X / x.rel, X, X_KIND), "Copy", auto_accept)


def handle_same_names(all_files, auto_accept):
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
        r = _interactive_pipeline(to_remove, remove_file, "Delete", auto_accept)
        removed.extend(r)

    return removed


def handle_duplicates(all_files, auto_accept):
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
        r = _interactive_pipeline(to_remove, remove_file, "Delete", auto_accept)
        removed.extend(r)

    return removed


def handle_permissions(file_entries, mode, auto_accept):
    invalid_files = [entry for entry in file_entries.values() if entry.mode != mode]
    print("Found {} file(s) with invalid permissions.".format(len(invalid_files)))
    return _interactive_pipeline(invalid_files, lambda x: chmod_file(x, mode), "CHMOD", auto_accept)


def handle_messy_files(file_entries, messy_chars, substitute, auto_accept):
    messy_files = [entry for entry in file_entries.values() if any(c in messy_chars for c in entry.name)]
    print("Found {} messy file(s)".format(len(messy_files)))
    return _interactive_pipeline(
        messy_files,
        lambda x: rename_file(x, find_new_name(x, messy_chars, substitute)),
        "Sanitize (replace messy chars with '{}')".format(substitute),
        auto_accept,
    )


def handle_temporary_files(file_entries, patterns, auto_accept):
    temporary_files = [
        entry for entry in file_entries.values() if any(fnmatch.fnmatch(entry.name, p) for p in patterns)
    ]
    print("Found {} temporary file(s).".format(len(temporary_files)))
    return _interactive_pipeline(temporary_files, remove_file, "Delete", auto_accept)


def handle_empty_files(file_entries, auto_accept):
    empty_files = [entry for entry in file_entries.values() if entry.size == 0]
    print("Found {} empty file(s).".format(len(empty_files)))
    return _interactive_pipeline(empty_files, remove_file, "Delete", auto_accept)


def _interactive_pipeline(entries, fn, action, auto_accept):
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
        answer = ask_user("What would you like to do?", list(inst.keys()), auto_accept)
        if answer != "p":
            break
        for entry in entries:
            print("-> File: {}".format(entry.path))

    if answer == "q":
        return []

    changes = []

    if answer == "y":
        for entry in entries:
            try:
                changes.append(fn(entry.path))
            except OSError as e:
                print("-> Error: {}".format(e))

    if answer == "i":
        for i, entry in enumerate(entries):
            answer = ask_user(
                "[{}/{}] File: {} {}? [y, N, q]".format(i + 1, n, entry.path, action),
                ["y", "N", "q"],
                auto_accept,
            )
            if answer == "y":
                try:
                    changes.append(fn(entry.path))
                except OSError as e:
                    print("-> Error: {}".format(e))

            if answer == "q":
                break

    return changes
