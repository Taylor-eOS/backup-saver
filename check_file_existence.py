import os

def find_files_not_in_second_folder(folder1, folder2):
    files_in_folder1 = set()
    for dirpath, _, filenames in os.walk(folder1):
        for filename in filenames:
            files_in_folder1.add(filename)
    missing_files = []
    files_in_folder2 = set()
    for dirpath, _, filenames in os.walk(folder2):
        for filename in filenames:
            files_in_folder2.add(filename)
    missing_files = list(files_in_folder1 - files_in_folder2)
    return missing_files

if __name__ == "__main__":
    folder1 = input("Source folder: ")
    folder2 = input("Target folder: ")
    missing_files = find_files_not_in_second_folder(folder1, folder2)
    if missing_files:
        print(f"Files in {folder1} but not in {folder2}:")
        for file in missing_files:
            print(file)
    else:
        print(f"All files in {folder1} are also present in {folder2}.")

