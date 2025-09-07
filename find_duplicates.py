import os
from collections import defaultdict

def find_duplicate_filenames(root_folder):
    filename_dict = defaultdict(list)
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            filename_dict[filename].append(dirpath)
    duplicate_files = {filename: paths for filename, paths in filename_dict.items() if len(paths) > 1}
    if duplicate_files:
        print("Filenames found in multiple folders:")
        for filename, paths in duplicate_files.items():
            print(f"\n{filename}:")
            for path in paths:
                print(f"  - {path}")
    else:
        print("No duplicate filenames found.")

if __name__ == "__main__":
    folder_to_check = input("Enter the folder path to check: ")
    find_duplicate_filenames(folder_to_check)

