import os


def remove_file(fpath):
    try:
        os.remove(fpath)
        print("-> {} deleted.".format(fpath))
        return {"path": fpath}

    except OSError as e:
        print("-> Error deleting {}: {}", fpath, e)
        return None


def apply_removed(all_files, changes):
    for item in changes:
        all_files.remove(item["path"])


def rename_file(fpath, new_fpath):
    try:
        os.rename(str(fpath), new_fpath)
        print("-> {} renamed to {}".format(fpath, new_fpath))
        return {"old_path": fpath, "new_path": new_fpath}

    except OSError:
        print("-> Error renaming {} to {}".format(fpath, new_fpath))
        return None


def apply_renamed(all_files, changes):
    for item in changes:
        all_files.remove(item["old_path"])
        all_files.add(item["new_path"])


def chmod_file(fpath, mode):
    try:
        os.chmod(fpath, mode)
        print("-> Changed mode of {} to {:o}".format(fpath, mode))
        return None
    except OSError:
        print("-> Error changing mode of {} to {:o}".format(fpath, mode))
        return None
