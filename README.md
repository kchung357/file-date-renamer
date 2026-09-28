# File Date Renamer

A Python command-line tool for renaming files based on their last modified timestamp and moving them to an output directory.

The renamed files use this format:

```text
YYYYMMDDHHMM####.ext
```

Example:

```text
photo.jpg --> 2026062014250000.jpg
document.pdf --> 2026062014310000.pdf
```

The final four digits are a counter. Each minute and extension starts at `0000`, and the next free number is used when that name already exists.

## Features

- Renames files using their last modified date and time
- Preserves the original file extension
- Moves renamed files to a selected output directory
- Skips an output name that already exists instead of overwriting it
- Skips folders automatically
- Supports a dry run that prints names without moving files
- Simple command-line interface
- Uses only Python standard-library modules

## Requirements

- Python 3.8 or newer

No external packages are required.

## Usage

Run the script with an input directory and output directory:

```bash
python rename.py -i /path/to/input -o /path/to/output
```

Example:

```bash
python rename.py -i ./input_files -o ./renamed_files
```

You can also use the long argument names:

```bash
python rename.py --input ./input_files --output ./renamed_files
```

Preview the new names without moving anything:

```bash
python rename.py -i ./input_files -o ./renamed_files --dry-run
```

## How It Works

The script:

1. Reads files from the input directory.
2. Skips subdirectories.
3. Gets each file's last modified timestamp.
4. Converts the timestamp into this format:

```text
YYYYMMDDHHMM
```

5. Adds a four-digit counter, starting at `0000` for that minute and extension.
6. Uses the next free counter when the output directory already has that name.
7. Preserves the original file extension.
8. Moves the renamed file to the output directory. `shutil.move` copies the file first when the output directory is on another filesystem.

## Example Output

```text
IMG_0012.JPG --> 2026062014250000.JPG
notes.txt --> 2026062014310000.txt
scan.pdf --> 2026062015080000.pdf
```

## Notes

This script moves files from the input directory to the output directory. It does not copy them.

If you want to keep the original files, make a backup before running the script, or pass `--dry-run` to preview the result.

A file that already has its target name is left in place. An existing file in the output directory is never replaced. If any file cannot be renamed, the command prints the error and exits with status 1. An invalid input or output directory exits with status 2.

## Privacy Notice

Do not commit private files, personal documents, photos, or sensitive data to this repository. This repository should contain only the script and project documentation.
