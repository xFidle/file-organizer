import os
from pathlib import Path


def remove_file(fpath: Path) -> bool:
    try:
        os.remove(fpath)
        print("-> {} deleted.".format(fpath))
        return True

    except OSError as e:
        print("-> Error deleting {}: {}", fpath, e)
        return False
