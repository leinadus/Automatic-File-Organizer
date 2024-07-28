import time
import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def generate_unique_filename(directory, filename):
    """
    Generate a unique filename by appending a number if a file with the same name already exists.
    """
    base, extension = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    while os.path.exists(os.path.join(directory, new_filename)):
        new_filename = f"{base} ({counter}){extension}"
        counter += 1
    return new_filename


class NewFileHandler(FileSystemEventHandler):
    def __init__(self, destination_directory, folders):
        self.destination_directory = destination_directory
        self.folders = folders

    def on_created(self, event):
        if event.is_directory:
            return
        self.process_file(event.src_path)

    def process_file(self, source_path):
        file_name = os.path.basename(source_path)
        file_extension = os.path.splitext(file_name)[1]

        # Determine the destination subdirectory based on the file extension
        if file_extension in [".txt", ".pdf", ".docx", ".xlsx", ".doc", ".ppt", ".odt", ".rtf", ".csv", ".xls", ".psd",
                              ".ai", ".sketch"]:
            subdirectory = self.folders[0]  # Documents
        elif file_extension in [".exe", ".msi", ".bat", ".sh", ".jar", ".apk", ".app"]:
            subdirectory = self.folders[1]  # Applications
        elif file_extension in [".jpg", ".png", ".webp", ".gif", ".bmp", ".tiff", ".tif", ".svg"]:
            subdirectory = self.folders[2]  # Photos
        elif file_extension in [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".mpeg", ".mp4v"]:
            subdirectory = self.folders[3]  # Videos
        elif file_extension in [".zip", ".rar", ".7z", ".tar", ".gz"]:
            subdirectory = self.folders[4]  # Archive
        elif file_extension in [".torrent", ".nzb"]:
            subdirectory = self.folders[5]  # Torrents
        else:
            subdirectory = ""

        destination_folder = os.path.join(self.destination_directory, subdirectory)
        destination_file_name = generate_unique_filename(destination_folder, file_name)
        destination_path = os.path.join(destination_folder, destination_file_name)

        os.makedirs(os.path.dirname(destination_folder), exist_ok=True)

        print(f"New file detected: {source_path}")
        print(f"File extension: {file_extension}")
        print(f"Moving file to: {destination_path}")

        try:
            if subdirectory != "":
                shutil.move(source_path, destination_path)
            print(f"Moved file: {source_path} to {destination_path}")
        except Exception as e:
            print(f"Failed to move file {source_path} to {destination_path}: {e}")


def monitor_directory(source_directory, destination_directory, folders):
    event_handler = NewFileHandler(destination_directory, folders)
    observer = Observer()
    observer.schedule(event_handler, source_directory, recursive=False)
    observer.start()
    print(f"Monitoring directory: {source_directory}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nMonitoring stopped.")
    observer.join()


def create_directories(base_directory, folder_names):
    for folder_name in folder_names:
        folder_path = os.path.join(base_directory, folder_name)
        try:
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                print(f"Successfully created: {folder_path}")
            else:
                print(f"Folder already exists: {folder_path}")
        except Exception as e:
            print(f"Error creating folder {folder_path}: {e}")


def load_directory_path(file_path):
    """
    Load the directory path from the file.
    """
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return f.read().strip()
    else:
        print(f"Path file {file_path} not found. Exiting.")
        exit(1)


if __name__ == "__main__":
    # Load the base directory path from the file
    base_directory_file = 'base_directory.txt'
    base_directory = load_directory_path(base_directory_file)

    folders = [
        "Documents",  # 0
        "Applications",  # 1
        "Photos",  # 2
        "Videos",  # 3
        "Archive",  # 4
        "Torrents",  # 5
    ]

    create_directories(base_directory, folders)
    monitor_directory(base_directory, base_directory, folders)
