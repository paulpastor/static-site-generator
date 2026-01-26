import os
import shutil
import sys

from markdown_blocks import markdown_to_html_node


def generate_pages_recursive(basepath, dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, item)

        if os.path.isfile(src_path):
            # only files should become .html
            dest_file = item
            if dest_file.endswith(".md"):
                dest_file = dest_file[:-3] + ".html"
            dest_path = os.path.join(dest_dir_path, dest_file)
            generate_page(basepath, src_path, template_path, dest_path)
        else:
            # recurse into subdirectories, mirroring structure
            new_dest_dir = os.path.join(dest_dir_path, item)
            generate_pages_recursive(basepath, src_path, template_path, new_dest_dir)


def generate_page(basepath, from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as f:
        markdown = f.read()

    with open(template_path) as f:
        template = f.read()

    html_node = markdown_to_html_node(markdown)
    html = html_node.to_html()

    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace("href=\\", f"href={basepath}")

    dirname = os.path.dirname(dest_path)
    if dirname and not os.path.exists(dirname):
        os.makedirs(dirname)

    with open(dest_path, "w") as f:
        f.write(template)


def extract_title(markdown):
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("Header was not found")


def copy_static_recursive(src_dir, dest_dir):
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)

    os.mkdir(dest_dir)

    items = os.listdir(src_dir)

    for item in items:
        src_path = os.path.join(src_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
        else:
            copy_static_recursive(src_path, dest_path)


def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    copy_static_recursive("static", "docs")
    generate_pages_recursive(basepath, "content", "template.html", "docs")


if __name__ == "__main__":
    main()
