# File Organizer

A command-line tool for scanning and cleaning up a file collection spread across multiple directories. Given a main directory **X** and one or more secondary directories **Y1, Y2, ...**, it detects issues and interactively proposes fixes.

## Usage

```
python3 src/main.py X Y1 [Y2 ...] [flags]
```

### Arguments

| Argument | Description |
|----------|-------------|
| `X` | Main directory — the canonical destination for all files |
| `Y1 Y2 ...` | One or more secondary directories to compare against X |

### Scan flags

Each flag enables one scan mode. Multiple flags can be combined in a single run.

| Flag | Description |
|------|-------------|
| `-e`, `--empty` | Find and delete empty files (size = 0) |
| `-t`, `--temporary` | Find and delete temporary files matching patterns from config (e.g. `*.tmp`, `*.bak`, `*~`) |
| `-m`, `--messy` | Find files whose names contain problematic characters and rename them, replacing those characters with the substitute from config |
| `-p`, `--permissions` | Find files whose permissions differ from the target mode in config and fix them |
| `-d`, `--duplicates` | Find files with identical content across all directories; suggest deleting all but the oldest (oldest = likely the original) |
| `-s`, `--same-names` | Find files sharing the same filename across directories; suggest deleting all but the newest |
| `-c`, `--copy` | Find files present in Y directories but missing from X and copy them into X, preserving relative paths |

### Execution flags

| Flag | Description |
|------|-------------|
| `--dry-run` | Simulate all actions without modifying anything on disk; prints what would be done |
| `--auto-accept` | Skip all prompts and automatically apply the default action for every file |

`--dry-run` and `--auto-accept` can be combined.

## Interactive prompts

When running without `--auto-accept`, each scan mode presents a menu before taking action:

```
[y] <action> all files
[N] Do nothing
[i] Inspect files one by one
[p] Print found files
[q] Quit
```

Choosing **i** (inspect) walks through each file individually and asks `[y, N, q]` per file.

## Examples

```bash
# Find and delete empty files in X and Y1, interactively
python3 src/main.py X Y1 --empty

# Remove temp files and fix permissions, auto-accepting everything
python3 src/main.py X Y1 -t --permissions --auto-accept

# Show what duplicates would be deleted without touching anything
python3 src/main.py X Y1 Y2 --duplicates --dry-run

# Full cleanup in one pass
python3 src/main.py X Y1 -e -t -m -p -d -s -c

# Copy all files missing from X, one by one inspection
python3 src/main.py X Y1 --copy
```

## Configuration

The tool reads `.clean_files` from the `$HOME/.config` directory. If file does
not exist it fallbacks to default config:

```
mode = 644
messy_chars = []:"'*?$#`|\ 
substitute = _
temp_patterns = *~;*.tmp;*.swp;*.bak
```

| Key | Description |
|-----|-------------|
| `mode` | Target file permission as an octal integer string (e.g. `644` = `rw-r--r--`) |
| `messy_chars` | String of individual characters considered problematic in filenames |
| `substitute` | Single character used to replace each problematic character |
| `temp_patterns` | Semicolon-separated glob patterns for temporary files |

## Running tests

```bash
# Run all tests
bash tests/test_all.sh

# Run a specific test
bash tests/test_empty.sh
```
Tests create temporary `X/`, `Y1/`, `Y2/` directories in the current working directory and clean up after themselves.

