#!/usr/bin/env python3

import os, shutil
from markdown_formatting import markdown_to_html_node, extract_title


# This function removes all files and subdirectories
# from the destination path and copies the files and
# subdirectories of the source path to the destination path.
def clean_and_copy_directory(src, dest):

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


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        md = f.read()
    with open(template_path) as f:
        html = f.read()
    node = markdown_to_html_node(md)
    content = node.to_html()
    title = extract_title(md)
    html = html.replace("{{ Title }}", title).replace("{{ Content }}", content)
    with open(dest_path, "w") as f:
        f.write(html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        if os.path.isdir(item_path):
            target_path = os.path.join(dest_dir_path, item)
            os.mkdir(target_path)
            generate_pages_recursive(item_path, template_path, target_path)
        else:
            target_name = ".".join(item.split(".")[:-1]) + ".html"
            target_path = os.path.join(dest_dir_path, target_name)
            generate_page(item_path, template_path, target_path)


def main():
    clean_and_copy_directory("static", "public")
    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()
