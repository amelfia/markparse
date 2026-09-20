import os
import shutil


def copy_files_recursive(src_dir_path, dst_dir_path):
    if not os.path.exists(dst_dir_path):
        os.mkdir(dst_dir_path)

    for entry in os.listdir(src_dir_path):
        from_path = os.path.join(src_dir_path, entry)
        dest_path = os.path.join(dst_dir_path, entry)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)

        else:
            copy_files_recursive(from_path, dest_path)



