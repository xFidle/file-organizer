import os
import shutil

from utils import Mode


def remove_file(fpath, exec_mode):
    try:
        if exec_mode not in (Mode.DryRun, Mode.Both):
            os.remove(fpath)
        print("-> {} deleted.".format(fpath))
        return {"path": fpath}
    except OSError as e:
        print("-> Error: {}".format(e))


def apply_removed(all_files, changes):
    for change in changes:
        all_files.pop(change["path"])


def rename_file(fpath, new_fpath, exec_mode):
    try:
        if exec_mode not in (Mode.DryRun, Mode.Both):
            os.rename(fpath, new_fpath)
        print("-> {} renamed to {}".format(fpath, new_fpath))
        return {"old_path": fpath, "new_path": new_fpath}
    except OSError as e:
        print("-> Error: {}".format(e))


def apply_renamed(all_files, changes):
    for change in changes:
        entry = all_files.pop(change["old_path"])
        new_path = change["new_path"]
        entry.name = new_path
        entry.rel = entry.rel.parent / new_path.name
        all_files[new_path] = entry


def chmod_file(fpath, mode, exec_mode):
    try:
        if exec_mode not in (Mode.DryRun, Mode.Both):
            os.chmod(fpath, mode)
        print("-> Changed mode of {} to {:o}".format(fpath, mode))
        return {"path": fpath, "mode": mode}
    except OSError as e:
        print("-> Error: {}".format(e))


def apply_chmod(all_files, changes):
    for change in changes:
        path = change["path"]
        all_files[path].mode = change["mode"]


def copy_file(src, dest, new_root, new_kind, exec_mode):
    try:
        if exec_mode not in (Mode.DryRun, Mode.Both):
            shutil.copy(src, dest)
        print("-> File moved from {} to {}".format(src, dest))
        return {"old_path": src, "new_path": dest, "new_root": new_root, "new_kind": new_kind}
    except OSError as e:
        print("-> Error: {}".format(e))


def apply_copied(all_files, changes):
    for change in changes:
        entry = change["old_path"]
        new_path = change["new_path"]
        new_root = change["new_root"]
        new_kind = change["new_kind"]
        entry.path = new_path
        entry.root = new_root
        entry.kind = new_kind
        entry.rel = new_path.relative_to(new_root)
        entry.name = new_path.name
        all_files[new_path] = entry
