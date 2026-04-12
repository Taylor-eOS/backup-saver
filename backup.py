import os
import shutil
import json
from datetime import datetime

SOURCE_DIR = os.path.expanduser('~/dv')
BACKUP_BASE_DIR = os.path.expanduser('~/Documents/backup/dv_backup/')
JSON_FILE = os.path.join(BACKUP_BASE_DIR, 'file_mod_times.json')
MAX_FILE_SIZE = 4000000 #3.8MB
EXTENSIONS = ('.py', '.json', '.txt')
SKIP_PREFIXES = ('input', 'output')

def load_mod_times():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_mod_times(file_mod_times):
    with open(JSON_FILE, 'w') as f:
        json.dump(file_mod_times, f, indent=4)

def should_skip(src_file, file_name):
    if not file_name.endswith(EXTENSIONS):
        return True
    if file_name.startswith(SKIP_PREFIXES):
        return True
    if os.path.getsize(src_file) > MAX_FILE_SIZE:
        print(f"Skipped (too large): {src_file.replace(SOURCE_DIR + '/', '')}")
        return True
    return False

def backup_dir_files(dir_path, backup_subdir, file_mod_times):
    files_copied = False
    for file_name in os.listdir(dir_path):
        src_file = os.path.join(dir_path, file_name)
        if should_skip(src_file, file_name):
            continue
        mod_time = os.path.getmtime(src_file)
        if src_file in file_mod_times and mod_time <= file_mod_times[src_file]:
            continue
        if not files_copied:
            os.makedirs(backup_subdir, exist_ok=True)
            files_copied = True
        shutil.copy2(src_file, os.path.join(backup_subdir, file_name))
        file_mod_times[src_file] = mod_time
        print(f"Backed up {src_file.replace(SOURCE_DIR + '/', '')}")

def run_backup():
    backup_dir = os.path.join(BACKUP_BASE_DIR, datetime.now().strftime("%Y%m%d_%H%M%S"))
    file_mod_times = load_mod_times()
    for entry in os.scandir(SOURCE_DIR):
        if entry.is_dir():
            backup_dir_files(entry.path, os.path.join(backup_dir, entry.name), file_mod_times)
    save_mod_times(file_mod_times)

if __name__ == "__main__":
    run_backup()

