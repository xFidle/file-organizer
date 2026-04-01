import hashlib
import os
from pathlib import Path


def ask_user(prompt: str, options: list[str]) -> str:
    while True:
        answer = input(prompt + " ")
        if answer.lower().strip() in options:
            return answer


def print_instruction(instruction: dict[str, str]) -> None:
    for key, info in instruction.items():
        print("[{}] {}".format(key, info))


def collect_files(directories: list[str]) -> list[Path]:
    result: list[Path] = []
    for dir in directories:
        for root, _, files in os.walk(dir, topdown=True):
            for fname in files:
                full_path = Path(root) / fname
                if full_path.is_file():
                    result.append(full_path)
    return result


def get_hash(fpath: Path, block_size: int = 1 << 16):
    sha256 = hashlib.sha256()
    with open(fpath, "rb") as f:
        for block in iter(lambda: f.read(block_size), b""):
            sha256.update(block)
    return sha256.hexdigest()
