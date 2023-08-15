import os
import argparse

header = f'''\
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

"""
TODO: 
NOTE:
"""
\n'''


def add_header(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(header + content)


def remove_header(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        new_content = content.replace(header, "", 1)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(new_content)


def process_directory(directory, operation):
    for root, dirs, files in os.walk(directory):
        for dir in dirs[:]:  # Using a copy of dirs list to iterate and modify it safely
            if dir == "__pycache__":
                dir_path = os.path.join(root, dir)
                delete_folder(dir_path)
                print(f"[OK] Deleted folder: {dir_path}")
                dirs.remove(
                    dir
                )  # Remove the folder from the list of directories to be further traversed
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                if operation == "add":
                    add_header(file_path)
                    print(f"[OK] Added header to {file_path}")
                elif operation == "remove":
                    remove_header(file_path)
                    print(f"[OK] Removed header from {file_path}")


def delete_folder(folder_path):
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)
        for dir in dirs:
            dir_path = os.path.join(root, dir)
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
    print(f"[DONE] Added the header to all files")
