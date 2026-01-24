import os
import shutil


def move_recursive(src_dir, dest_dir):
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
            move_recursive(src_path, dest_path)


def main():
    move_recursive("static", "public")


main()
