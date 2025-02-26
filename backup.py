import os
import shutil
from datetime import datetime
import json

source_dir = os.path.expanduser('~/dv')
backup_base_dir = os.path.expanduser('~/Documents/backup/development/')
backup_dir = os.path.join(backup_base_dir, datetime.now().strftime("%Y%m%d_%H%M%S"))
json_file = os.path.join(backup_base_dir, 'file_mod_times.json')

if os.path.exists(json_file):
    with open(json_file, 'r') as f:
        file_mod_times = json.load(f)
else:
    file_mod_times = {}

def save_mod_times():
    with open(json_file, 'w') as f:
        json.dump(file_mod_times, f, indent=4)

for root, dirs, files in os.walk(source_dir):
    if root == source_dir:
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            backup_subdir = os.path.join(backup_dir, dir_name)
            files_copied = False
            for file in os.listdir(dir_path):
                if file.endswith(('.py', '.json', '.txt')):
                    src_file = os.path.join(dir_path, file)
                    mod_time = os.path.getmtime(src_file)
                    if src_file not in file_mod_times or mod_time > file_mod_times[src_file]:
                        if not files_copied:
                            os.makedirs(backup_subdir, exist_ok=True)
                            files_copied = True
                        dst_file = os.path.join(backup_subdir, file)
                        shutil.copy2(src_file, dst_file)
                        file_mod_times[src_file] = mod_time
                        src_file = src_file.replace("/home/l/dv/", "")
                        print(f"Backed up {src_file}")
    break

save_mod_times()
