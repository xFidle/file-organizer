import argparse
from pathlib import Path

from commands import apply_chmod, apply_removed, apply_renamed
from config import (
    get_duplicates_fallback,
    get_messy_chars,
    get_mode,
    get_same_names_fallback,
    get_substitute_char,
    get_temp_patterns,
    load_config,
)
from funcs import (
    handle_duplicates,
    handle_empty_files,
    handle_messy_files,
    handle_permissions,
    handle_same_names,
    handle_temporary_files,
)
from utils import collect_files


def get_sys_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("X", help="Main directory directory")
    parser.add_argument("Y", nargs="+", help="Additional dirs to compare against X [Y1, Y2, ...]")
    parser.add_argument("--auto-accept", action="store_true", help="Auto accept default action, don't ask for input")
    parser.add_argument("-e", "--empty", action="store_true", help="Delete empty files")
    parser.add_argument("-t", "--temporary", action="store_true", help="Delete temporary files")
    parser.add_argument("-m", "--messy", action="store_true", help="Sanitize messy files")
    parser.add_argument("-p", "--permissions", action="store_true", help="Change permissons")
    parser.add_argument("-d", "--duplicates", action="store_true", help="Delete duplicates (keep oldest)")
    parser.add_argument("-s", "--same-names", action="store_true", help="Delete files with same names (keep newest)")
    return parser.parse_args()


def main(args):
    X, Y = Path(args.X), list(map(Path, args.Y))
    print(X, Y)
    all_files = collect_files(X, Y)
    config = load_config(".clean_files")
    aa = args.auto_accept

    if args.empty:
        changes = handle_empty_files(all_files, aa)
        apply_removed(all_files, changes)

    if args.temporary:
        changes = handle_temporary_files(all_files, get_temp_patterns(config), aa)
        apply_removed(all_files, changes)

    if args.messy:
        changes = handle_messy_files(all_files, get_messy_chars(config), get_substitute_char(config), aa)
        apply_renamed(all_files, changes)

    if args.permissions:
        changes = handle_permissions(all_files, get_mode(config), aa)
        apply_chmod(all_files, changes)

    if args.duplicates:
        changes = handle_duplicates(all_files, args.X, Path(args.X) / get_duplicates_fallback(config), aa)
        apply_removed(all_files, changes)

    if args.same_names:
        changes = handle_same_names(all_files, args.X, Path(args.X) / get_same_names_fallback(config), aa)
        apply_removed(all_files, changes)


if __name__ == "__main__":
    main(get_sys_args())
