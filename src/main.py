#!/usr/bin/env python3

import os, sys, shutil
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
def copy_files(src, dest):
    if not os.path.exists(dest):
        os.mkdir(dest)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)

        # If the entry is a directory, copy it and copy the files/dirs inside recursively
        if os.path.isdir(src_path):
            if not os.path.exists(dest_path):
                os.mkdir(dest_path)
            copy_files(src_path, dest_path)
        else:
            # for a file, just copy
            shutil.copy(src_path, dest_path)


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        md = f.read()
    with open(template_path) as f:
        html = f.read()
    node = markdown_to_html_node(md)
    content = node.to_html()
    title = extract_title(md)
    html = html.replace("{{ Title }}", title).replace("{{ Content }}", content)
    # Replace basepath from href and src
    html = html.replace('href="/', f'href="{basepath}').replace(
        'src="/', f'src="{basepath}'
    )
    with open(dest_path, "w") as f:
        f.write(html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        if os.path.isdir(item_path):
            target_path = os.path.join(dest_dir_path, item)
            if not os.path.exists(target_path):
                os.mkdir(target_path)
            generate_pages_recursive(item_path, template_path, target_path, basepath)
        else:
            target_name = ".".join(item.split(".")[:-1]) + ".html"
            target_path = os.path.join(dest_dir_path, target_name)
            generate_page(item_path, template_path, target_path, basepath)


def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    clean_and_copy_directory("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    main()
