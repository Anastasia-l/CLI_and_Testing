import os
import shutil
import re
from datetime import datetime


# Copy file
def copy_file(filename, directory_name):
    full_file_path = os.path.join(directory_name, filename)
    destination_path = input("Where to copy the file to? ")

    if os.path.isfile(full_file_path):
        try:
            shutil.copy2(full_file_path, destination_path)
            print(f"The file {filename} was successfully copied! Check that out!")
        except:
            print(f"Error copying the file {filename}")

    else:
        print(f"The file {filename} could not be found!")


# Remove file or directory
def removing(filename, directory_name):
    if not os.path.isdir(directory_name):
        print("The directory was not found or doesn`t exist")
        return  # Exit the function early if the directory doesn`t exist`

    # Check if the file exists
    if filename:  # Only check for files if filename is provided
        full_file_path = os.path.join(directory_name, filename)
        if os.path.isfile(full_file_path):
            try:
                os.remove(full_file_path)
                print(f"The file {filename} was successfully deleted from the directory")
            except FileNotFoundError:
                print(f"The file {filename} was not found")
        else:
            print("The file was not found or doesn`t exist!")
    else:
        # If there`s no filename provided attempt to delete a directory
        try:
            os.rmdir(directory_name)
            print(f"The directory {directory_name} was successfully deleted!")
        except:
            print("The directory was not discovered or some error!")


# Count the amount of files in the directory
def counting_files(directory_name):
    count = 0
    for root, dirs, files in os.walk(directory_name):
        count += len(files)
    print(f"The amount of files in the directory: {directory_name}: {count}")


# Find the files that match a regex
def find_matching_files(directory, pattern):
    regex = re.compile(pattern, re.IGNORECASE)
    matches = []

    try:
        print(f"Searching in directory: {directory}...")

        for root, _, files in os.walk(directory):
            for file in files:
                full_path = os.path.join(root, file)
                if regex.search(file):
                    matches.append(full_path)
    except Exception as e:
        print(f"Error while searching {e}")

    return matches


# Get file birthday
use_recursive = True


def get_file_birthday(full_path):
    timestamp = os.path.getctime(full_path)
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")


def rename_file_with_date(full_path):
    base_name, extension = os.path.splitext(os.path.basename(full_path))
    parent_folder = os.path.dirname(full_path)

    new_name = f"{base_name}_{get_file_birthday(full_path)}{extension}"
    new_full_path = os.path.join(parent_folder, new_name)

    os.rename(full_path, new_full_path)
    print(f"Renamed: {os.path.basename(full_path)} -> {new_name}")


def process_folder(folder_path, recursive=False):
    if recursive:
        for root, _, files in os.walk(folder_path):
            for file in files:
                rename_file_with_date(os.path.join(root, file))
    else:
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                rename_file_with_date(item_path)


def format_size(size):
    if size < 1024:
        return f"{size} B"
    elif size < 1024 * 1024:
        return f"{size / 1024:.2f} KB"
    elif size < 1024 * 1024 * 1024:
        return f"{size / (1024 * 1024):.2f} MB"
    elif size < 1024 * 1024 * 1024 * 1024:
        return f"{size / (1024 * 1024 * 1024):.2f} GB"
    else:
        return "Some mistake occured"


def analyzing_directory(directory_name):
    full_size = 0
    size = 0

    for item in os.listdir(directory_name):
        item_path = os.path.join(directory_name, item)
        if os.path.isfile(item_path):
            size = os.path.getsize(item_path)
        elif os.path.isdir(item_path):
            for dirpath, _, filenames in os.walk(item_path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    size += os.path.getsize(filepath)

        else:
            size = 0

        full_size += size
        print(f"> - {item} {format_size(size)}")

    print(f"> - Full size of the files: {format_size(full_size)}")

    return full_size
