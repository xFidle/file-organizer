import argparse

from commands import apply_removed, apply_renamed
from config import get_messy_chars, get_mode, get_substitute_char, get_temp_patterns, load_config
from funcs import handle_duplicates, handle_empty_files, handle_messy_files, handle_permissions, handle_temporary_files
from utils import collect_files, get_home_path


def get_sys_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("X", help="X directory")
    parser.add_argument("Y", help="Y directory")
    parser.add_argument("--dirs", nargs="+", help="Additional dirs to scan")
    parser.add_argument("-e", "--empty", action="store_true", help="Delete empty files")
    parser.add_argument("-t", "--temporary", action="store_true", help="Delete temporary files")
    parser.add_argument("-m", "--messy", action="store_true", help="Sanitize messy files")
    parser.add_argument("-p", "--permissions", action="store_true", help="Change permissons")
    parser.add_argument("-d", "--duplicates", action="store_true", help="Delete duplicates")
    return parser.parse_args()


def main(args):
    all_directories = [args.X, args.Y]
    if args.dirs is not None:
        all_directories += args.dirs
    all_files = collect_files(all_directories)
    config = load_config(get_home_path() / ".clean_files")

    if args.empty:
        changes = handle_empty_files(all_files)
        apply_removed(all_files, changes)

    if args.temporary:
        changes = handle_temporary_files(all_files, get_temp_patterns(config))
        apply_removed(all_files, changes)

    if args.messy:
        changes = handle_messy_files(all_files, get_messy_chars(config), get_substitute_char(config))
        apply_renamed(all_files, changes)

    if args.permissions:
        handle_permissions(all_files, get_mode(config))

    if args.duplicates:
        changes = handle_duplicates(all_files)
        apply_removed(all_files, changes)


if __name__ == "__main__":
    main(get_sys_args())
