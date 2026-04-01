from pathlib import Path

from commands import remove_file
from utils import ask_user, print_instruction


def handle_duplicates(files: list[Path]) -> None:
    pass


def handle_empty_files(files: list[Path]) -> None:
    empty_files = [f for f in files if f.stat().st_size == 0]
    n = len(empty_files)

    print("Found {} empty file(s).".format(n))

    if not empty_files:
        return

    inst = {
        "y": "Delete all empty files permamently",
        "N": "Do nothing",
        "i": "Inspect files one by one",
    }

    print_instruction(inst)
    answer = ask_user("What would you like to do?", list(inst.keys()))

    if answer == "y":
        for file in empty_files:
            remove_file(file)

    if answer == "i":
        for file in empty_files:
            answer = ask_user("File: {}. Delete? [y, N, q]".format(file), ["y", "N", "q"])
            if answer == "y":
                remove_file(file)

            if answer == "q":
                break
