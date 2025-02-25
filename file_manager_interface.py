import argparse
import sys
import file_manager_functions
import os


def handle_command(args):
    if args.command == "copy":
        file_manager_functions.copy_file(args.filename, args.directory_name)
    elif args.command == "count":
        file_manager_functions.counting_files(args.directory_name)
    elif args.command == "find":
        matches = file_manager_functions.find_matching_files(args.directory, args.pattern)
        print(f"Files matching '{args.pattern}': {matches}")
    elif args.command == "creation_date":
        date = file_manager_functions.get_file_birthday(args.full_path)
        print(f"Creation date of {args.full_path}: {date}")
    elif args.command == "rename_file_with_date":
        if not os.path.exists(args.folder_path):
            print("Sorry, but this file or folder doesn`t exist!")
            return
        confirm = input("This will rename your file name! Type 'YES' to continue: ")
        if confirm.lower() == "yes":
            file_manager_functions.rename_file_with_date(args.folder_path)
        else:
            print("Cancelled by user")
    elif args.command == "rename_files_with_date":
        if not os.path.exists(args.folder_path):
            print("Sorry, but this folder doesn`t exist!")

        else:
            confirm = input("This will rename all the files in your folder! Type 'YES' to continue: ")
            if confirm.lower() == "yes":
                file_manager_functions.process_folder(args.folder_path, recursive=args.recursive)
                print(f"All the files in {args.folder_path} were succesfully renamed!")
    elif args.command == "remove":
        file_manager_functions.removing(args.filename, args.directory_name)
    elif args.command == "analyze":
        file_manager_functions.analyzing_directory(args.directory_name)
    else:
        print("Invalid command. Use --help for more instructions")


def main():
    parser = argparse.ArgumentParser(description="A simple file manager for managing files and directories")

    # Add commands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: Copy file
    copy_parser = subparsers.add_parser("copy", help="Copy a file to destination")
    copy_parser.add_argument("filename", help="Full path to the file")
    copy_parser.add_argument("directory_name", help="Name of the directory where to copy the file to")

    # Command: Count files in directory
    count_parser = subparsers.add_parser("count", help="Count the number of files in the directory")
    count_parser.add_argument("directory_name", help="Directory to count files in")

    # Command: Remove a file or a directory
    remove_parser = subparsers.add_parser("remove", help="Remove a file or directory")
    remove_parser.add_argument("filename", nargs="?", default=None, help="Name of the file or directory to delete")
    remove_parser.add_argument("directory_name", help="Directory where the file or directory is located")

    # Command: Find files matching a regex
    find_parser = subparsers.add_parser("find", help="Find files matching a regex pattern")
    find_parser.add_argument("directory", help="Directory to search in")
    find_parser.add_argument("pattern", help="Regex pattern to match")

    # Command: Get creation date of a file
    date_parser = subparsers.add_parser("creation_date", help="Get the creation date of a file")
    date_parser.add_argument("full_path", help="Full filename to get creation date for")

    # Command: Rename with date for the folder
    rename_folder_date_parser = subparsers.add_parser("rename_file_with_date",
                                                      help="Rename your file or folder with the creation date at the end of it")
    rename_folder_date_parser.add_argument("folder_path",
                                           help="Path to the file or the folder that you want to be renamed")

    # Command: Rename with date for the files in the folder recursively
    rename_files_date_parser = subparsers.add_parser("rename_files_with_date",
                                                     help="Rename all the files in the folder")
    rename_files_date_parser.add_argument("folder_path", help="Path to the folder where you want your files renamed")
    rename_files_date_parser.add_argument("--recursive", action="store_true", help="Process files recursively")

    # Command: Analyze files` and folders` sizes
    analyze_size_parser = subparsers.add_parser("analyze",
                                                help="Analyze the files` sizes and the full size of the folder")
    analyze_size_parser.add_argument("directory_name",
                                     help="Directory where you want to analyze the sizes of the files")

    # Parse arguments
    args = parser.parse_args()

    # If no command is provided, -> help
    if not args.command:
        parser.print_help()
        sys.exit(1)

    handle_command(args)


if __name__ == "__main__":
    main()
