import os
import shutil

from utils import generate_unique_path, get_hash


def remove_file(fpath):
    os.remove(fpath)
    print("-> {} deleted.".format(fpath))
    return {"path": fpath}


def apply_removed(all_files, changes):
    for change in changes:
        all_files.pop(change["path"])


def rename_file(fpath, new_fpath):
    os.rename(fpath, new_fpath)
    print("-> {} renamed to {}".format(fpath, new_fpath))
    return {"old_path": fpath, "new_path": new_fpath}


def apply_renamed(all_files, changes):
    for change in changes:
        entry = all_files.pop(change["old_path"])
        new_path = change["new_path"]
        entry.name = new_path
        entry.rel = entry.rel.parent / new_path.name
        all_files[new_path] = entry


def chmod_file(fpath, mode):
    os.chmod(fpath, mode)
    print("-> Changed mode of {} to {:o}".format(fpath, mode))
    return {"path": fpath, "mode": mode}


def apply_chmod(all_files, changes):
    for change in changes:
        path = change["path"]
        all_files[path].mode = change["mode"]


def move_file(src, dest, new_root, new_kind):
    shutil.move(src, dest)
    print("-> File moved from {} to {}".format(src, dest))
    return {"old_path": src, "new_path": dest, "new_root": new_root, "new_kind": new_kind}


def move_file_safely(src, dest, fallback_dir, new_root, new_kind):
    try:
        if not dest.exists():
            dest.parent.mkdir(parents=True, exist_ok=True)
            return move_file(src, dest, new_root, new_kind)

        elif get_hash(src) != get_hash(dest):
            dest.parent.mkdir(parents=True, exist_ok=True)
            fallback_dir.mkdir(parents=True, exist_ok=True)
            to = generate_unique_path(fallback_dir / dest.name)
            return move_file(src, to, new_root, new_kind)

        return {"skipped": True}


def apply_moved(all_files, changes):
    for change in changes:
        entry = all_files.pop(change["old_path"])
        new_path = change["new_path"]
        new_root = change["new_root"]
        new_kind = change["new_kind"]
        entry.path = new_path
        entry.root = new_root
        entry.kind = new_kind
        entry.rel = new_path.relative_to(new_root)
        entry.name = new_path.name
        all_files[new_path] = entry
