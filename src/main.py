#!/usr/bin/env python3

import os, shutil


# This function removes all files and subdirectories
# from the destination path and copies the files and
# subdirectories of the source path to the destination path.
def clean_and_copy_directory(src, dest):
    # Check that source and destination exists
    if not os.path.exists(src):
        raise Exception("source path does not exist")
    if not os.path.exists(dest):
        raise Exception("destination path does not exist")

    # Remove everything from the destination
    print(f"Cleaning and copying from {src}/ to {dest}/...")
    remove_files(dest)
    copy_files(src, dest)
    print("Done!")


# Removes files recursively from the target path
def remove_files(path):
    if path_list := os.listdir(path):
        for entry in path_list:
            entry_path = os.path.join(path, entry)
            # Recurse deeper if it is a directory, then remove directory
            if os.path.isdir(entry_path):
                remove_files(entry_path)
                os.rmdir(entry_path)
            # Remove the file if it is not a directory
            else:
                os.remove(entry_path)


# This function copies files recursively from source destination to target destination
def copy_files(src, dest, depth=0):
    # Shared path between source and dest, starts at "."
    if not depth:
        shared_path = ""
    else:
        shared_path = os.path.join(*src.split("/")[-depth:])
    path_list = os.listdir(src)
    for entry in path_list:
        entry_path = os.path.join(src, entry)

        # If the entry is a directory, copy it and copy the files/dirs inside recursively
        if os.path.isdir(entry_path):
            os.mkdir(os.path.join(dest, entry))
            copy_files(entry_path, os.path.join(dest, shared_path), depth + 1)
        else:
            shutil.copy(entry_path, os.path.join(dest, shared_path))


def main():
    clean_and_copy_directory("static", "public")


if __name__ == "__main__":
    main()
