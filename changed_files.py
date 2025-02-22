import os
import sys
import time

target_folder = "~/dv"
if len(sys.argv) != 2:
    print("Usage: python script.py <reference_file_or_unix_timestamp>")
    sys.exit(1)
arg = sys.argv[1]
try:
    if os.path.exists(arg):
        ref_time = os.path.getmtime(arg)
    else:
        ref_time = float(arg)
except:
    print("Invalid argument. Provide a valid Unix timestamp.")
    sys.exit(1)
dv_dir = os.path.expanduser(target_folder)
for subdir in os.listdir(dv_dir):
    subdir_path = os.path.join(dv_dir, subdir)
    if os.path.isdir(subdir_path):
        for file in os.listdir(subdir_path):
            if file.endswith(('.py', '.txt', '.json')):
                file_path = os.path.join(subdir_path, file)
                if os.path.getmtime(file_path) > ref_time:
                    print(file_path)

