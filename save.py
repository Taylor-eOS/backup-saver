import os
import shutil
from datetime import datetime
import filecmp

dirs_to_backup = ['~/Desktop', '~/Documents', '~/home']
dirs_to_backup = [os.path.expanduser(d) for d in dirs_to_backup]
backup_base_dir = os.path.expanduser('~/backup')
backup_dir = os.path.expanduser(f'{backup_base_dir}/{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}')
os.makedirs(backup_dir, exist_ok=True)
exclude_extensions = ['.desktop']

def file_changed(src, previous_backups):
    for backup in previous_backups:
        prev_src = os.path.join(backup, os.path.basename(src))
        if os.path.exists(prev_src) and filecmp.cmp(src, prev_src, shallow=False):
            return False
    return True

previous_backups = [os.path.join(backup_base_dir, d) for d in os.listdir(backup_base_dir)
                    if os.path.isdir(os.path.join(backup_base_dir, d)) and os.path.join(backup_base_dir, d) != backup_dir]

for dir_to_backup in dirs_to_backup:
    if os.path.exists(dir_to_backup):
        for root, dirs, files in os.walk(dir_to_backup):
            for file in files:
                if any(file.endswith(ext) for ext in exclude_extensions):
                    continue
                src_file = os.path.join(root, file)
                if file_changed(src_file, previous_backups):
                    dst_file = os.path.join(backup_dir, os.path.basename(src_file))
                    shutil.copy2(src_file, dst_file)
