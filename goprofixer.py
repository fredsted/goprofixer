import os
import re
import subprocess
import sys
from collections import defaultdict
import platform
import shutil
import time
import datetime

def copy_creation_date(source_path, target_path):
        stat = os.stat(source_path)
        atime = stat.st_atime
        mtime = stat.st_mtime

        # Set access and modified time (note: most systems don't allow setting creation time directly)
        os.utime(target_path, (atime, mtime))

        # On macOS, use `SetFile` to adjust the creation date (optional)
        if platform.system() == 'Darwin':
            created = datetime.datetime.fromtimestamp(stat.st_ctime).strftime('%m/%d/%Y %H:%M:%S')
            os.system(f'SetFile -d "{created}" "{target_path}"')

def find_gopro_groups(folder_path):
    """
    Groups GoPro video segments by base filename number (e.g., 1234 from GOPR1234.MP4, GP011234.MP4)
    """
    segment_pattern = re.compile(r'(?:GOPR|GP|GX\d{2})(\d{4})\.MP4$', re.IGNORECASE)
    groups = defaultdict(list)

    for file in os.listdir(folder_path):
        if file.upper().endswith(".MP4"):
            match = segment_pattern.search(file)
            if match:
                base_id = match.group(1)
                groups[base_id].append(file)

    # Sort each group by filename
    for key in groups:
        groups[key].sort()
    return groups

def write_file_list(folder, group_id, group_files):
    path = os.path.join(folder, 'file_list_%s.txt' % group_id)
    with open(path, 'w') as f:
        for video in group_files:
            full_path = os.path.join(folder, video)
            f.write(f"file '{full_path}'\n")
    return path

def merge_group(folder, group_id, files):
    print(f"Merging session {group_id} with {len(files)} files...")
    list_path = write_file_list(folder, group_id, files)
    output_file = os.path.join(folder, f"{group_id}.mp4")

    command = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", list_path,
        "-c", "copy",
        output_file
    ]

    subprocess.run(command)
    os.remove(list_path)

    # Copy creation date from the first file in the group
    source_file = os.path.join(folder, files[0])
    copy_creation_date(source_file, output_file)

    print(f"Created: {output_file}")

def ask_folder_mac():
    """Uses AppleScript to open a folder picker and return the selected folder path (macOS only)."""
    try:
        script = 'choose folder with prompt "Select GoPro Video Folder"'
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            return None
        # osascript returns a POSIX-style path with colons (e.g., Macintosh HD:Users:Name:Folder)
        folder = result.stdout.strip().replace("alias ", "").replace(":", "/").replace("Macintosh HD", "")
        return "/Volumes" + folder if folder.startswith("/Volumes") else folder
    except Exception as e:
        print(f"Error opening folder picker: {e}")
        return None

def main():
    if len(sys.argv) == 2:
        folder = sys.argv[1]
    else:
        print("No folder path provided. Opening folder picker...")
        folder = ask_folder_mac()

    if not os.path.isdir(folder):
        print("Invalid folder path.")
        return

    groups = find_gopro_groups(folder)
    if not groups:
        print(f"No GoPro video segments found at {folder}.")
        return

    for group_id, files in groups.items():
        merge_group(folder, group_id, files)

if __name__ == "__main__":
    main()
