import argparse

from funcs import handle_empty_files
from utils import collect_files


def get_sys_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("dirs", nargs="+", help="Directories to scan")
    parser.add_argument("-e", "--empty", action="store_true", help="Remove empty files")
    return parser.parse_args()


def main(args: argparse.Namespace) -> None:
    all_files = collect_files(args.dirs)

    if args.empty:
        handle_empty_files(all_files)


if __name__ == "__main__":
    main(get_sys_args())
