import os
import shutil

def copy_subfolder_files(subfolder_path, src_folder, dest_folder, copied_filenames):
    for dirpath, _, filenames in os.walk(subfolder_path):
        for filename in filenames:
            relative_path = os.path.relpath(dirpath, src_folder)
            dest_subfolder = os.path.join(dest_folder, relative_path)
            os.makedirs(dest_subfolder, exist_ok=True)
            dest_file = os.path.join(dest_subfolder, filename)
            if filename in copied_filenames:
                print(f"Skipping {dest_file} (file already copied from recent)")
                continue
            try:
                shutil.copy2(os.path.join(dirpath, filename), dest_file)
                copied_filenames.add(filename)
                print(f"Copied {os.path.join(dirpath, filename)} to {dest_file}")
            except Exception as e:
                print(f"Error copying {os.path.join(dirpath, filename)}: {e}")

def copy_files_priority(src_folder, dest_folder):
    copied_filenames = set()
    subdirs = [d for d in os.listdir(src_folder) if os.path.isdir(os.path.join(src_folder, d))]
    recent_folder = None
    archive_folder = None
    for d in subdirs:
        lower_d = d.lower()
        if "recent" in lower_d:
            recent_folder = os.path.join(src_folder, d)
        elif "archive" in lower_d:
            archive_folder = os.path.join(src_folder, d)
    if recent_folder:
        print("Processing recent folder")
        copy_subfolder_files(recent_folder, src_folder, dest_folder, copied_filenames)
    else:
        print("Recent folder not found in source.")
    if archive_folder:
        print("Processing archive folder")
        copy_subfolder_files(archive_folder, src_folder, dest_folder, copied_filenames)
    else:
        print("Archive folder not found in source.")

if __name__ == "__main__":
    source_folder = input("Source folder: ")
    destination_folder = input("Destination folder: ")
    copy_files_priority(source_folder, destination_folder)

