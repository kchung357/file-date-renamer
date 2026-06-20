import os
import argparse
import random
from datetime import datetime

def rename_files(input_directory, output_directory):
    """
    Renames files in the input directory based on their last modified date and time,
    and moves the renamed files to the output directory.
    """
    files = os.listdir(input_directory)

    for file in files:
        file_path = os.path.join(input_directory, file)
        
        # Check if the current item is a file
        if not os.path.isfile(file_path):
            continue
        
        try:
            # Get the file's last modified time
            modified_time = os.path.getmtime(file_path)
            modified_datetime = datetime.fromtimestamp(modified_time)

            # Generate the new filename based on the modified date and time
            new_filename = (
                f"{modified_datetime.year}"
                f"{modified_datetime.month:02d}"
                f"{modified_datetime.day:02d}"
                f"{modified_datetime.hour:02d}"
                f"{modified_datetime.minute:02d}"
                f"{random.randint(0, 9999):04d}"
                f"{os.path.splitext(file)[1]}"
            )

            # Construct the new file path in the output directory
            new_file_path = os.path.join(output_directory, new_filename)
            
            # Move the file to the output directory with the new filename
            os.rename(file_path, new_file_path)
            print(f"{file} --> {new_filename}")
        except Exception as e:
            print(f"{file} cannot be renamed. Error: {str(e)}")

def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Rename files based on their last modified date and time.")
    
    # Add command-line arguments
    parser.add_argument("-i", "--input", required=True, help="Directory containing the files to be renamed")
    parser.add_argument("-o", "--output", required=True, help="Directory to move the renamed files to")
    
    # Parse the command-line arguments
    args = parser.parse_args()

    input_directory = args.input
    output_directory = args.output

    # Check if the input and output directories exist
    if not os.path.isdir(input_directory):
        print(f"Invalid input directory: {input_directory}")
        parser.print_help()
        return
    
    if not os.path.isdir(output_directory):
        print(f"Invalid output directory: {output_directory}")
        parser.print_help()
        return

    # Call the rename_files function with the input and output directories
    rename_files(input_directory, output_directory)

if __name__ == "__main__":
    main()