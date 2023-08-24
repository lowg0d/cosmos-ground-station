"""
This Script adds a header with copyright information to all the python files, also provides
functions to remove it, it also deletes all the pycaches files.add

add <directory> - override files with it, an add it to the ones that don't, remove pycache folders
remove <directory> - remove the header from all the files
"""
import os
import argparse

HEADER = """\
######################### Xnxe9 <3? #########################
#
#   .o88b.  .d88b.  .d8888. .88b  d88.  .d88b.  .d8888.
#  d8P  Y8 .8P  Y8. 88'  YP 88'YbdP`88 .8P  Y8. 88'  YP
#  8P      88    88 `8bo.   88  88  88 88    88 `8bo.
#  8b      88    88   `Y8b. 88  88  88 88    88   `Y8b.
#  Y8b  d8 `8b  d8' db   8D 88  88  88 `8b  d8' db   8D
#   `Y88P'  `Y88P'  `8888Y' YP  YP  YP  `Y88P'  `8888Y'
# 
# ★ StarLab RPL - COSMOS GROUND STATION ★
# Communications and Observation Station for Mission Operations and Surveillance
#
# By Martin Ortiz
# Version 1.0.0
# Date 06.08.2023
#
#############################################################
\n"""


def add_header(file_path):
    """Adds the predefined header to a file."""
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(HEADER + content)


def remove_header(file_path):
    """Removes the predefined header from a file."""
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        new_content = content.replace(HEADER, "", 1)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(new_content)


def process_directory(directory, operation):
    """Processes all Python files in a directory."""
    for root, dirs, files in os.walk(directory):
        for _dir in dirs[:]:
            if _dir == "__pycache__":
                dir_path = os.path.join(root, _dir)
                delete_folder(dir_path)
                dirs.remove(_dir)
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                if operation == "add":
                    remove_header(file_path)
                    add_header(file_path)
                elif operation == "remove":
                    remove_header(file_path)


def delete_folder(folder_path):
    """Recursively deletes a folder and its contents."""
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)
        for _dir in dirs:
            dir_path = os.path.join(root, _dir)
            os.rmdir(dir_path)
    os.rmdir(folder_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Add or remove header from Python files."
    )
    parser.add_argument(
        "operation",
        choices=["add", "remove"],
        help="Operation to perform: add or remove",
    )
    parser.add_argument("target_directory", help="Path to the target directory")
    args = parser.parse_args()

    process_directory(args.target_directory, args.operation)
