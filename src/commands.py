import os
import shutil

from utils import generate_unique_path, get_hash


def remove_file(fpath):
    try:
        os.remove(fpath)
        print("-> {} deleted.".format(fpath))
        return {"path": fpath}

    except OSError as e:
        print("-> Error deleting {}: {}", fpath, e)
        return None


def apply_removed(all_files, changes):
    removed_paths = {ch["path"] for ch in changes}
    all_files[:] = [entry for entry in all_files if entry["path"] not in removed_paths]


def rename_file(fpath, new_fpath):
    try:
        os.rename(fpath, new_fpath)
        print("-> {} renamed to {}".format(fpath, new_fpath))
        return {"old_path": fpath, "new_path": new_fpath}

    except OSError:
        print("-> Error renaming {} to {}".format(fpath, new_fpath))
        return None


def apply_renamed(all_files, changes):
    changes_by_old_path = {ch["old_path"]: ch for ch in changes}
    for entry in all_files:
        change = changes_by_old_path.get(entry["path"])
        if change is None:
            continue
        new_path = change["new_path"]
        entry["path"] = new_path
        entry["name"] = new_path.name
        entry["rel"] = entry["rel"].parent / new_path.name


def chmod_file(fpath, mode):
    try:
        os.chmod(fpath, mode)
        print("-> Changed mode of {} to {:o}".format(fpath, mode))
        return {"path": fpath, "mode": mode}
    except OSError:
        print("-> Error changing mode of {} to {:o}".format(fpath, mode))
        return None


def apply_chmod(all_files, changes):
    changes_by_path = {ch["path"]: ch for ch in changes}
    for entry in all_files:
        change = changes_by_path.get(entry["path"])
        if change is None:
            continue
        entry["mode"] = change["mode"]


def move_file(src, dest):
    try:
        shutil.move(src, dest)
        print("-> File moved from {} to {}".format(src, dest))
        return {"old_path": src, "new_path": dest}
    except Exception:
        print("-> Error moving file from {} to {}".format(src, dest))
        return None


def move_file_safely(src, dest, fallback_dir):
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        return move_file(src, dest)

    elif get_hash(src) != get_hash(dest):
        dest.parent.mkdir(parents=True, exist_ok=True)
        fallback_dir.mkdir(parents=True, exist_ok=True)
        to = generate_unique_path(fallback_dir / dest.name)
        return move_file(src, to)

    return {"skipped": True}
