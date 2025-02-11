import os
import shutil
import argparse
import hashlib
from datetime import datetime, timedelta

def get_desktop_path():
    """
    Returns the default Desktop path.
    Works for most systems where the Desktop is located at ~/Desktop.
    """
    return os.path.join(os.path.expanduser("~"), "Desktop")

def sort_files(directory):
    """
    Sorts files in the given directory into folders based on their file extension.
    Files with unrecognized extensions are moved into an "Others" folder.
    """
    categories = {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"],
        "Documents": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx"],
        "Videos": [".mp4", ".avi", ".mov", ".wmv", ".flv", ".mkv"],
        "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg"],
        "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
        "Executables": [".exe", ".msi", ".bat", ".sh"],
        "Scripts": [".py", ".js", ".rb", ".php", ".pl"],
    }
    
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        # Skip directories (you might also want to extend this to skip already sorted folders)
        if os.path.isdir(file_path):
            continue
        
        file_ext = os.path.splitext(filename)[1].lower()
        moved = False
        for category, extensions in categories.items():
            if file_ext in extensions:
                dest_dir = os.path.join(directory, category)
                os.makedirs(dest_dir, exist_ok=True)
                try:
                    shutil.move(file_path, os.path.join(dest_dir, filename))
                    print(f"Moved {filename} to {category}")
                except Exception as e:
                    print(f"Error moving {filename}: {e}")
                moved = True
                break
        
        if not moved:
            dest_dir = os.path.join(directory, "Others")
            os.makedirs(dest_dir, exist_ok=True)
            try:
                shutil.move(file_path, os.path.join(dest_dir, filename))
                print(f"Moved {filename} to Others")
            except Exception as e:
                print(f"Error moving {filename}: {e}")

def hash_file(file_path):
    """
    Returns the MD5 hash of the file located at file_path.
    """
    hasher = hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            # Read and update hash in chunks to handle large files.
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    return hasher.hexdigest()

def remove_duplicates(directory):
    """
    Scans the given directory (including subdirectories) for duplicate files.
    Duplicate files (files with the same hash) are removed.
    """
    file_hashes = {}
    duplicates = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                file_hash = hash_file(file_path)
            except Exception as e:
                print(f"Error hashing file {file_path}: {e}")
                continue
            if file_hash in file_hashes:
                duplicates.append(file_path)
            else:
                file_hashes[file_hash] = file_path

    for dup in duplicates:
        try:
            os.remove(dup)
            print(f"Removed duplicate file: {dup}")
        except Exception as e:
            print(f"Error removing file {dup}: {e}")

def remove_old_files(directory, days=30):
    """
    Removes files that have not been modified in the last 'days' days.
    """
    now = datetime.now()
    threshold = now - timedelta(days=days)
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                if mtime < threshold:
                    os.remove(file_path)
                    print(f"Deleted old file: {file_path}")
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Desktop Cleaner Script")
    parser.add_argument("--path", type=str, default=get_desktop_path(),
                        help="Path to clean (default: Desktop)")
    parser.add_argument("--sort", action="store_true",
                        help="Sort files into categories based on their type")
    parser.add_argument("--dedupe", action="store_true",
                        help="Remove duplicate files")
    parser.add_argument("--remove-old", type=int, metavar="DAYS",
                        help="Remove files older than the specified number of days")
    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"Path {args.path} does not exist.")
        return

    if args.sort:
        print("Sorting files...")
        sort_files(args.path)
    if args.dedupe:
        print("Removing duplicate files...")
        remove_duplicates(args.path)
    if args.remove_old:
        print(f"Removing files older than {args.remove_old} days...")
        remove_old_files(args.path, days=args.remove_old)

if __name__ == "__main__":
    main()
