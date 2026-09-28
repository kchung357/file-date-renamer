import os
import sys
import argparse
from datetime import datetime
from shutil import move


def allocate_name(output_directory, source, modified_datetime, extension, next_index):
    """Return the next free YYYYMMDDHHMM#### name for this timestamp and extension."""
    stamp = modified_datetime.strftime("%Y%m%d%H%M")
    key = (stamp, extension)
    number = next_index.get(key, 0)

    while number < 10000:
        filename = f"{stamp}{number:04d}{extension}"
        number += 1
        destination = os.path.join(output_directory, filename)
        same_file = os.path.abspath(destination) == os.path.abspath(source)
        if same_file or not os.path.lexists(destination):
            next_index[key] = number
            return filename

    raise OSError(f"no free filename left for {stamp}{extension}")


def rename_files(input_directory, output_directory, dry_run=False):
    """Rename files from their last-modified time and move them to output_directory."""
    next_index = {}
    renamed = 0
    skipped = 0
    failed = 0

    for name in sorted(os.listdir(input_directory)):
        source = os.path.join(input_directory, name)
        if not os.path.isfile(source):
            skipped += 1
            continue

        try:
            modified = datetime.fromtimestamp(os.path.getmtime(source))
            extension = os.path.splitext(name)[1]
            new_name = allocate_name(
                output_directory, source, modified, extension, next_index
            )
            destination = os.path.join(output_directory, new_name)

            if os.path.abspath(destination) == os.path.abspath(source):
                skipped += 1
                continue

            if not dry_run:
                move(source, destination)
            print(f"{name} --> {new_name}")
            renamed += 1
        except OSError as error:
            failed += 1
            print(f"{name} cannot be renamed. Error: {error}", file=sys.stderr)

    action = "would rename" if dry_run else "renamed"
    print(f"{renamed} {action}, {skipped} skipped, {failed} failed")
    return failed


def main():
    parser = argparse.ArgumentParser(
        description="Rename files based on their last modified date and time."
    )
    parser.add_argument("-i", "--input", required=True, help="Directory containing the files to be renamed")
    parser.add_argument("-o", "--output", required=True, help="Directory to move the renamed files to")
    parser.add_argument("-n", "--dry-run", action="store_true", help="Show the new names without moving files")
    args = parser.parse_args()

    if not os.path.isdir(args.input):
        parser.error(f"Invalid input directory: {args.input}")
    if not os.path.isdir(args.output):
        parser.error(f"Invalid output directory: {args.output}")

    if rename_files(args.input, args.output, dry_run=args.dry_run):
        sys.exit(1)


if __name__ == "__main__":
    main()
