# File Date Renamer

A Python command-line tool for renaming files based on their last modified timestamp and moving them to an output directory.

The renamed files use this format:

```text
YYYYMMDDHHMM####.ext
```

Example:

```text
photo.jpg --> 2026062014250387.jpg
document.pdf --> 2026062014318842.pdf
```

The final four digits are random numbers added to reduce filename collisions.

## Features

- Renames files using their last modified date and time
- Preserves the original file extension
- Moves renamed files to a selected output directory
- Skips folders automatically
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

## How It Works

The script:

1. Reads files from the input directory.
2. Skips subdirectories.
3. Gets each file's last modified timestamp.
4. Converts the timestamp into this format:

```text
YYYYMMDDHHMM
```

5. Adds a random four-digit number.
6. Preserves the original file extension.
7. Moves the renamed file to the output directory.

## Example Output

```text
IMG_0012.JPG --> 2026062014250387.JPG
notes.txt --> 2026062014318842.txt
scan.pdf --> 2026062015082291.pdf
```

## Notes

This script moves files from the input directory to the output directory. It does not copy them.

If you want to keep the original files, make a backup before running the script.

## Privacy Notice

Do not commit private files, personal documents, photos, or sensitive data to this repository. This repository should contain only the script and project documentation.
